from typing import List

import cvxpy as cp
import numpy as np

from entities.problem_data import ProblemData
from entities.requesting import Queue, QueueRequest, User
from problems.appointment_multistation import AppointmentMultiStation
from problems.highs_test import HighsTest

if __name__ == '__main__':
    queues: List[Queue] = [Queue.random() for i in range(5)]
    users: List[User] = [User.random() for i in range(37)]

    i = 0
    for queue in queues:
        for user in users:
            i = i + 1
            if i % 4 == 0:
                req = QueueRequest(user, queue)

    problem_data = ProblemData(queues, users)
    problem_data.process()

    problem = AppointmentMultiStation(problem_data)
    problem.compile_and_solve()

    # had 4 seconds for 35 users on 5 queues
