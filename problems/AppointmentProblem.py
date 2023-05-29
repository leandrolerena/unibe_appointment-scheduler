from abc import abstractmethod

import cvxpy as cp


class AppointmentProblem:
    @abstractmethod
    def compile_and_solve(self) -> cp.Problem:
        pass
