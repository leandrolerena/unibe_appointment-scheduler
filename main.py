import os
from typing import List

import cvxpy as cp
import numpy as np

from entities.problem_data import ProblemData
from entities.requesting import Queue, QueueRequest, User
from plotting.plot_queue_perspective import PlotQueuePerspective
from plotting.plot_user_perspective import PlotUserPerspective
from problems.appointment_multistation import AppointmentMultiStation
from problems.highs_test import HighsTest

if __name__ == '__main__':
    queues: List[Queue] = [Queue.random() for i in range(5)]
    users: List[User] = [User.random() for i in range(21)]

    i = 0
    for queue in queues:
        for user in users:
            i = i + 1
            # Make it a bit "sparser" - not all users go to all queues
            if i % 4 == 0:
                req = QueueRequest(user, queue)

    problem_data = ProblemData(queues, users, "Test")
    problem_data.process()

    problem = AppointmentMultiStation(problem_data)
    problem.compile_and_solve()

    out_dir = f"out/{problem_data.scenario_name.strip().replace('/', '_').replace(' ', '_')}"
    os.makedirs(out_dir, exist_ok=True)

    try:
        queue_plot = PlotQueuePerspective(problem_data)
        queue_plot.plot_gnt(out_dir)

        user_plot = PlotUserPerspective(problem_data)
        user_plot.plot_gnt(out_dir)
    except Exception as e:
        print("Could not create plots")

    problem_data.gen_code()

    if problem_data.check_feasibility() == True:
        print("Additional Feasibility Check passed")
    else:
        raise Exception("Problem is not feasible")

    # todo: presentation: ideal scenario (good distribution
    # todo: presentation: all on the same

    # todo: queue -> "appointment scheduling"
    # todo: overall setting, but in programm we can prune a lot of constraints

    # todo: for non-zero energy, search goes on -> no high config...
    # todo: for zero energy, the problem is **much** faster

    # todo: next steps

    # had 4 seconds for 35 users on 5 queues
