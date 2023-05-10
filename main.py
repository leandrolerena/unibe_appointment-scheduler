import cvxpy as cp
import numpy as np

from problems.appointment_multistation import AppointmentMultiStation
from problems.highs_test import HighsTest

if __name__ == '__main__':
    problem = AppointmentMultiStation(3, [((1, 100), 3), ((1, 100), 3), ((1, 100), 3)])
    prob = problem.compile_problem()

    # Solve with SciPy/HiGHS.
    prob.solve(solver=cp.SCIPY, scipy_options={"method": "highs"})
    print("optimal value with SciPy/HiGHS:", prob.value)

