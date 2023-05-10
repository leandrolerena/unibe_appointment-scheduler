import cvxpy as cp
import numpy as np

from problems.ProblemBuilder import ProblemBuilder


class AppointmentMultiStation(ProblemBuilder):
    def __init__(self, n_stations, n_persons):
        self.K = n_stations
        self.N = n_persons

    def compile_problem(self) -> cp.Problem:
        N = self.N
        K = self.K
        t_k = 10
        M = 1000

        # variables
        c_per_user = [cp.Variable([N, K]) for i in range(N)]
        x_per_user = [cp.Variable([N, K], boolean=True) for i in range(N)]
        b_per_user = [cp.Variable([K, K], boolean=True) for i in range(N)]

        s_per_queue = [cp.Variable(N) for k in range(K)]

        # constraints
        no_queue_overlaps = [s_per_queue[k][j] + t_k <= s_per_queue[k][j + 1] for j in range(N - 1) for k in range(K)]
        no_cross_queue_overlaps = [s_per_queue[k][j]
                                   <= s_per_queue[k_prime][j_prime] + M *
                                   (3 - x_per_user[i][j][k] - x_per_user[i][j_prime][k_prime] - b_per_user[i][k][
                                       k_prime])
                                   for j in range(N - 1)
                                   for j_prime in range(N - 1)
                                   for k in range(K)
                                   for k_prime in range(K)
                                   for i in range(N)
                                   if k != k_prime]

        b_symmetry = [b_per_user[i][k][k_prime] == 1 - b_per_user[i][k_prime][k]
                      for k in range(K)
                      for k_prime in range(K)
                      for i in range(N)
                      if k != k_prime]

        b_diagonal = [b_per_user[i][k][k] == 0 for k in range(K) for i in range(N)]

        one_user_per_spot_in_queue = [cp.sum([x_per_user[i][j][k] for i in range(N)]) == 1 for j in range(N) for k in range(K)]
        user_enqueued_once_in_queue = [cp.sum([x_per_user[i][j][k] for j in range(N)]) == 1 for i in range(N) for k in range(K)]

        c_positive = [c >= np.zeros(c.shape) for c in c_per_user]

        c_penalty_to_early = []
        c_penalty_to_late = []

        # objective
        obj = cp.Minimize(sum([cp.sum(c) for c in c_per_user]))

        constraints = []
        constraints.extend(no_queue_overlaps)
        constraints.extend(no_cross_queue_overlaps)
        constraints.extend(b_symmetry)
        constraints.extend(b_diagonal)
        constraints.extend(one_user_per_spot_in_queue)
        constraints.extend(user_enqueued_once_in_queue)
        constraints.extend(c_positive)

        prob = cp.Problem(obj, constraints)
        return prob
