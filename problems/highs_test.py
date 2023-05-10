import cvxpy as cp
import numpy as np

from problems.ProblemBuilder import ProblemBuilder


class HighsTest(ProblemBuilder):
    def __init__(self, c: float):
        self.c = c

    def compile_problem(self) -> cp.Problem:
        two = np.ones(2) * 2
        x = cp.Variable(2)
        obj = cp.Minimize(x[0] * self.c + cp.norm(x, 1))
        constraints = [x >= two]
        # or constraints = [x >= 2]
        prob = cp.Problem(obj, constraints)
        return prob

