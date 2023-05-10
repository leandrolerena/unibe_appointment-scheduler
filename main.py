from typing import List

import cvxpy as cp
import numpy as np

from entities.queue import Queue
from entities.user import User
from problems.appointment_multistation import AppointmentMultiStation
from problems.highs_test import HighsTest

if __name__ == '__main__':
    queues: List[Queue] = [Queue(time_serving=10), Queue(time_serving=10), Queue(time_serving=10)]
    users: List[User] = [User(earliest=0, latest=100), User(earliest=0, latest=100), User(earliest=0, latest=100)]

    problem = AppointmentMultiStation(queues, users)
    prob = problem.compile_and_solve()



