import time
from typing import List

import cvxpy as cp
import numpy as np

from entities.queue import Queue
from entities.user import User
from problems.AppointmentProblem import AppointmentProblem

TimePreferences = tuple[int, int]
Gamma = int
UserPreferences = tuple[TimePreferences, Gamma]


class AppointmentMultiStation(AppointmentProblem):
    def __init__(self, queues: List[Queue], users: List[User], transitivity_elimination=False):
        self.K = len(queues)
        self.N = len(users)
        self.users = users
        self.queues = queues

        self.transitivity_elimination = transitivity_elimination
        # TODO: add queue opening time

    def compile_and_solve(self) -> cp.Problem:
        N = self.N
        K = self.K
        t_k = 10
        M = 1000

        start = time.time()
        # variables
        c_per_user = [cp.Variable([N, K]) for i in range(N)]
        x_per_user = [cp.Variable([N, K], boolean=True) for i in range(N)]
        b_per_user = [cp.Variable([K, K], boolean=True) for i in range(N)]

        s_per_queue = [cp.Variable(N) for k in range(K)]

        # constraints
        no_queue_overlaps = [s_per_queue[k][j] + t_k <= s_per_queue[k][j + 1] for j in range(N - 1) for k in range(K)]
        no_cross_queue_overlaps = [s_per_queue[k][j] + t_k
                                   <= s_per_queue[k_prime][j_prime] + M *
                                   (3 - x_per_user[i][j][k] - x_per_user[i][j_prime][k_prime] - b_per_user[i][k][
                                       k_prime])
                                   for j in range(N)
                                   for j_prime in range(N)
                                   for k in range(K)
                                   for k_prime in range(K)
                                   for i in range(N)
                                   if k != k_prime]

        b_symmetry = [b_per_user[i][k][k_prime] == 1 - b_per_user[i][k_prime][k]
                      for k in range(K)
                      for k_prime in range(K)
                      for i in range(N)
                      if k != k_prime]

        b_transitivity = [b_per_user[i][a][b] + b_per_user[i][b][c] - 1 <=  b_per_user[i][a][c]
                          for i in range(N)
                          for a in range(K)
                          for b in range(K)
                          for c in range(K)
                          if a != b and b != c]


        b_diagonal = [b_per_user[i][k][k] == 0 for k in range(K) for i in range(N)]

        one_user_per_spot_in_queue = [cp.sum([x_per_user[i][j][k] for i in range(N)]) == 1 for j in range(N) for k in
                                      range(K)]
        user_enqueued_once_in_queue = [cp.sum([x_per_user[i][j][k] for j in range(N)]) == 1 for i in range(N) for k in
                                       range(K)]

        c_positive = [c >= np.zeros(c.shape) for c in c_per_user]

        c_penalty_to_early = [c_per_user[i][j][k] >= self.users[i].earliest - s_per_queue[k][j] - M * (1 - x_per_user[i][j][k])
                              for i in range(N)
                              for j in range(N)
                              for k in range(K)]

        c_penalty_to_late =  [c_per_user[i][j][k] >= s_per_queue[k][j] + t_k - self.users[i].latest - M * (1 - x_per_user[i][j][k])
                              for i in range(N)
                              for j in range(N)
                              for k in range(K)]

        # objective
        obj = cp.Minimize(sum([cp.sum(c) for c in c_per_user]))

        constraints = []
        constraints.extend(no_queue_overlaps)
        constraints.extend(no_cross_queue_overlaps)
        constraints.extend(b_symmetry)
        if self.transitivity_elimination:
            constraints.extend(b_transitivity)
        constraints.extend(b_diagonal)
        constraints.extend(one_user_per_spot_in_queue)
        constraints.extend(user_enqueued_once_in_queue)
        constraints.extend(c_positive)
        constraints.extend(c_penalty_to_early)
        constraints.extend(c_penalty_to_late)

        prob = cp.Problem(obj, constraints)

        end = time.time()

        print(f"processed constraints in {end-start} seconds")
        # Solve with SciPy/HiGHS.
        start = time.time()
        prob.solve(solver=cp.SCIPY, scipy_options={"method": "highs"})
        print("optimal value with SciPy/HiGHS:", prob.value)
        print(f"Problem status: {prob.status}")

        end = time.time()
        for i in range(N):
            for k in range(K):
                for j in range(N):
                    if x_per_user[i].value[j][k] == 1:
                        print(f"User {i} visists queue {k} at {'{:.2f}'.format(s_per_queue[k].value[j])} with cost {'{:.2f}'.format(c_per_user[i].value[j][k])}")

        print(f"Total time used: {end-start} seconds")
        # TODO: Put results in queue about ordering
        # TODO: Put cost to user

        return prob

