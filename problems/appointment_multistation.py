import math
import time
from typing import List

import cvxpy as cp
import numpy as np

from entities.problem_data import ProblemData
from entities.requesting import Queue, User
from problems.AppointmentProblem import AppointmentProblem

TimePreferences = tuple[int, int]
Gamma = int
UserPreferences = tuple[TimePreferences, Gamma]


class AppointmentMultiStation(AppointmentProblem):
    """
    Problem formulation for the appointment multi-stations (=services) problem
    """
    def __init__(self, problem_data: ProblemData):
        self.users: List[User] = problem_data.users
        self.queues: List[Queue] = problem_data.queues
        self.problem_data = problem_data

    def compile_and_solve(self) -> cp.Problem:
        print("Constraints calculation")

        # a sufficiently high number to deactivate the constraints, at the moment set to the ending time
        # this is a bit dirty sorry
        M = 1000

        start = time.time()

        # variables
        c_per_queue = [cp.Variable([len(queue.requests), len(queue.requests)]) for queue in self.queues]
        x_per_queue = [cp.Variable([len(queue.requests), len(queue.requests)], boolean=True) for queue in self.queues]
        b_per_user = [cp.Variable([len(user.requests), len(user.requests)], boolean=True) for user in self.users]

        s_per_queue = [cp.Variable(len(queue.requests)) for queue in self.queues]

        # constraints
        spots_after_opening = [s_per_queue[k][0] >= self.queues[k].opening for k in
                               range(len(self.queues))]

        spots_before_closing = [s_per_queue[k][-1] + self.queues[k].time_serving <= self.queues[k].closing for k in
                                range(len(self.queues))]

        no_queue_overlaps = [s_per_queue[k][j] + self.queues[k].time_serving <= s_per_queue[k][j + 1] for k in
                             range(len(self.queues)) for j in range(len(self.queues[k].requests) - 1)]

        no_cross_queue_overlaps = []

        # here we generate no-cross-queue-overlap constraints according to the specification (see slides)
        # we add only the necessary constraints (meaning we do not add the constraints which are always deactivated
        # by the big-M method

        for queue in self.queues:
            for queue_prime in self.queues:
                if queue.index == queue_prime.index:
                    continue

                for user in self.users:
                    if user.queue_index.get(queue.index) is not None and user.queue_index.get(
                            queue_prime.index) is not None:
                        # here we know that user is in both queues, so proceed
                        for j_in_queue in range(len(queue.requests)):
                            for j_in_queue_prime in range(len(queue_prime.requests)):
                                # so add the constraints
                                no_cross_queue_overlaps.append(s_per_queue[queue.index][j_in_queue] + queue.time_serving
                                                               <= s_per_queue[queue_prime.index][j_in_queue_prime]
                                                               + M * (3 - x_per_queue[queue.index][
                                    user.queue_index[queue.index]][j_in_queue]
                                                                      - x_per_queue[queue_prime.index][
                                                                          user.queue_index[queue_prime.index]][
                                                                          j_in_queue_prime]
                                                                      - b_per_user[user.index][
                                                                          queue.user_index[user.index]][
                                                                          queue_prime.user_index[user.index]]
                                                                      )

                                                               )

        # Symmetry constraint for the b-variables
        b_symmetry = [b_per_user[i][k][k_prime] == 1 - b_per_user[i][k_prime][k]
                      for i in range(len(self.users))
                      for k in range(len(self.users[i].requests))
                      for k_prime in range(len(self.users[i].requests))
                      if k != k_prime]

        # Transitivity constraint for the b-variables
        b_transitivity = [b_per_user[i][a][b] + b_per_user[i][b][c] - 1 <= b_per_user[i][a][c]
                          for i in range(len(self.users))
                          for a in range(len(self.users[i].requests))
                          for b in range(len(self.users[i].requests))
                          for c in range(len(self.users[i].requests))
                          if len(self.users[i].requests) >= 3
                          if (a < b < c)]

        # The "diagonal" of the b-variables: k comes before k is always false
        b_diagonal = [b_per_user[i][k][k] == 0
                      for i in range(len(self.users))
                      for k in range(len(self.users[i].requests))]

        # the two constraints from the assignment problem
        one_user_per_spot_in_queue = [cp.sum([x_per_queue[k][i][j] for i in range(len(self.queues[k].requests))]) == 1
                                      for k in range(len(self.queues))
                                      for j in range(len(self.queues[k].requests))]

        user_enqueued_once_in_queue = [cp.sum([x_per_queue[k][i][j] for j in range(len(self.queues[k].requests))]) == 1
                                       for k in range(len(self.queues))
                                       for i in range(len(self.queues[k].requests))
                                       ]

        # Cost definition (positive, deadzone)
        c_positive = [c >= np.zeros(c.shape) for c in c_per_queue]

        c_penalty_to_early = [
            c_per_queue[k][i][j] >= self.queues[k].requests[i].earliest - s_per_queue[k][j] - M * (
                        1 - x_per_queue[k][i][j])
            for k in range(len(self.queues))
            for i in range(len(self.queues[k].requests))
            for j in range(len(self.queues[k].requests))
        ]

        c_penalty_to_late = [
            c_per_queue[k][i][j] >= s_per_queue[k][j] + self.queues[k].time_serving - self.queues[k].requests[
                i].latest - M * (
                    1 - x_per_queue[k][i][j])
            for k in range(len(self.queues))
            for i in range(len(self.queues[k].requests))
            for j in range(len(self.queues[k].requests))]

        # objective
        obj = cp.Minimize(sum([cp.sum(c) for c in c_per_queue]))

        constraints = []
        constraints.extend(spots_after_opening)
        constraints.extend(spots_before_closing)
        constraints.extend(no_queue_overlaps)
        constraints.extend(no_cross_queue_overlaps)
        constraints.extend(b_symmetry)
        constraints.extend(b_transitivity)
        constraints.extend(b_diagonal)
        constraints.extend(one_user_per_spot_in_queue)
        constraints.extend(user_enqueued_once_in_queue)
        constraints.extend(c_positive)
        constraints.extend(c_penalty_to_early)
        constraints.extend(c_penalty_to_late)

        prob = cp.Problem(obj, constraints)

        end = time.time()

        print(f"processed {len(constraints)} constraints in {end - start} seconds")
        # Solve with SciPy/HiGHS.
        start = time.time()
        # passing args to highs is not supported
        # prob.solve(solver=cp.SCIPY, scipy_options={"method": "highs"}, options={"maxiter": 100, "disp": True})
        prob.solve(solver=cp.SCIPY, scipy_options={"method": "highs"})
        print("optimal value with SciPy/HiGHS:", prob.value)
        print(f"Problem status: {prob.status}")

        end = time.time()

        # Parse the results and put back to problem_data
        for k in range(len(self.queues)):
            queue = self.queues[k]
            for i in range(len(queue.requests)):
                request = queue.requests[i]
                for j in range(len(queue.requests)):
                    if math.isclose(x_per_queue[k].value[i][j], 1):
                        user = self.users[request.user_index]
                        print(
                            f"User {user.index} visists queue {k} at {'{:.2f}'.format(s_per_queue[k].value[j])} until {'{:.2f}'.format(s_per_queue[k].value[j] + self.queues[k].time_serving)} with cost {'{:.2f}'.format(c_per_queue[k].value[i][j])}")
                        request.optimal_visiting_time = s_per_queue[k].value[j]
                        request.visiting_duration = self.queues[k].time_serving

        print(f"Total time used: {end - start} seconds")
        self.problem_data.solution_time = end - start
        self.problem_data.solution_cost = prob.value
        return prob
