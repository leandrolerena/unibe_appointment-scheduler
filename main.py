from typing import List

import cvxpy as cp
import numpy as np

from entities.queue import Queue, QueueRequest, User
from problems.appointment_multistation import AppointmentMultiStation
from problems.highs_test import HighsTest

if __name__ == '__main__':
    # queues: List[Queue] = [Queue(time_serving=10), Queue(time_serving=10), Queue(time_serving=10)]
    # users: List[User] = [User(earliest=0, latest=30), User(earliest=0, latest=100), User(earliest=0, latest=100)]

    queues: List[Queue] = [Queue.random() for i in range(3)]
    users: List[User] = [User.random() for i in range(3)]

    for user in users:
        queue = queues[0]
        req = QueueRequest(user, queue)
        queue.add_request(req)
        user.add_request(req)

    queue = queues[1]
    user = users[1]
    req = QueueRequest(users[1], queue)
    queue.add_request(req)
    user.add_request(req)

    queue = queues[2]
    user = users[2]
    req = QueueRequest(users[2], queue)
    queue.add_request(req)
    user.add_request(req)

    problem = AppointmentMultiStation(queues, users)
    problem.compile_and_solve()



