from abc import abstractmethod

import cvxpy as cp
import numpy as np

class ProblemBuilder:
    @abstractmethod
    def compile_problem(self) -> cp.Problem:
        pass