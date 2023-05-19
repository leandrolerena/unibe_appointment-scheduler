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
    def __init__(self, problem_data: ProblemData, transitivity_elimination=False):
        self.users: List[User] = problem_data.users
        self.queues: List[Queue] = problem_data.queues

        self.transitivity_elimination = transitivity_elimination
        # TODO: add queue opening time

    def compile_and_solve(self) -> cp.Problem:
        print("Constraints calculation")
        M = 19 * 60

        start = time.time()
        # variables
        c_per_queue = [cp.Variable([len(queue.requests), len(queue.requests)]) for queue in self.queues]
        x_per_queue = [cp.Variable([len(queue.requests), len(queue.requests)], boolean=True) for queue in self.queues]
        b_per_user = [cp.Variable([len(user.requests), len(user.requests)], boolean=True) for user in self.users]

        s_per_queue = [cp.Variable(len(queue.requests)) for queue in self.queues]

        # constraints
        no_queue_overlaps = [s_per_queue[k][j] + self.queues[k].time_serving <= s_per_queue[k][j + 1] for k in
                             range(len(self.queues)) for j in range(len(self.queues[k].requests) - 1)]

        no_cross_queue_overlaps = []

        for queue in self.queues:
            for queue_prime in self.queues:
                if queue.index == queue_prime.index:
                    continue

                # todo: which users are in both queues
                for user in self.users:
                    if user.queue_index.get(queue.index) is not None and user.queue_index.get(
                            queue_prime.index) is not None:
                        # here we know that user is in both queues
                        for j_in_queue in range(len(queue.requests)):
                            for j_in_queue_prime in range(len(queue_prime.requests)):
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

        b_symmetry = [b_per_user[i][k][k_prime] == 1 - b_per_user[i][k_prime][k]
                      for i in range(len(self.users))
                      for k in range(len(self.users[i].requests))
                      for k_prime in range(len(self.users[i].requests))
                      if k != k_prime]

        # b_transitivity = [b_per_user[i][a][b] + b_per_user[i][b][c] - 1 <=  b_per_user[i][a][c]
        #                   for i in range(N)
        #                   for a in range(K)
        #                   for b in range(K)
        #                   for c in range(K)
        #                   if a != b and b != c]

        b_diagonal = [b_per_user[i][k][k] == 0
                      for i in range(len(self.users))
                      for k in range(len(self.users[i].requests))]

        one_user_per_spot_in_queue = [cp.sum([x_per_queue[k][i][j] for i in range(len(self.queues[k].requests))]) == 1
                                      for k in range(len(self.queues))
                                      for j in range(len(self.queues[k].requests))]

        user_enqueued_once_in_queue = [cp.sum([x_per_queue[k][i][j] for j in range(len(self.queues[k].requests))]) == 1
                                       for k in range(len(self.queues))
                                       for i in range(len(self.queues[k].requests))
                                       ]

        c_positive = [c >= np.zeros(c.shape) for c in c_per_queue]

        c_penalty_to_early = [
            c_per_queue[k][i][j] >= self.users[i].earliest - s_per_queue[k][j] - M * (1 - x_per_queue[k][i][j])
            for k in range(len(self.queues))
            for i in range(len(self.queues[k].requests))
            for j in range(len(self.queues[k].requests))
        ]

        c_penalty_to_late = [
            c_per_queue[k][i][j] >= s_per_queue[k][j] + self.queues[k].time_serving - self.users[i].latest - M * (
                    1 - x_per_queue[k][i][j])
            for k in range(len(self.queues))
            for i in range(len(self.queues[k].requests))
            for j in range(len(self.queues[k].requests))]

        # objective
        obj = cp.Minimize(sum([cp.sum(c) for c in c_per_queue]))

        constraints = []
        constraints.extend(no_queue_overlaps)
        constraints.extend(no_cross_queue_overlaps)
        constraints.extend(b_symmetry)
        if self.transitivity_elimination:
            pass
            # constraints.extend(b_transitivity)
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
        prob.solve(solver=cp.SCIPY, scipy_options={"method": "highs"}, options={"maxiter": 100, "disp": True})
        print("optimal value with SciPy/HiGHS:", prob.value)
        print(f"Problem status: {prob.status}")

        end = time.time()

        for k in range(len(self.queues)):
            queue = self.queues[k]
            for i in range(len(queue.requests)):
                request = queue.requests[i]
                for j in range(len(queue.requests)):
                    if math.isclose(x_per_queue[k].value[i][j], 1):
                        user = self.users[request.user_index]
                        print(
                            f"User {user.index} visists queue {k} at {'{:.2f}'.format(s_per_queue[k].value[j])} until {'{:.2f}'.format(s_per_queue[k].value[j] + self.queues[k].time_serving)} with cost {'{:.2f}'.format(c_per_queue[k].value[i][j])}")

        print(f"Total time used: {end - start} seconds")
        # TODO: Put results in queue about ordering
        # TODO: Put cost to user

        return prob
