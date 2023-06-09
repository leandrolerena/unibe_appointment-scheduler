import os
from typing import List

from entities.problem_data import ProblemData
from entities.requesting import Queue, User, QueueRequest
from plotting.plot_queue_perspective import PlotQueuePerspective
from plotting.plot_user_perspective import PlotUserPerspective
from problems.appointment_multistation import AppointmentMultiStation

queues: List[Queue] = []
users: List[User] = []
queue_0 = Queue(7, 0, 1000)
queues.append(queue_0)
queue_1 = Queue(24, 0, 1000)
queues.append(queue_1)
queue_2 = Queue(25, 0, 1000)
queues.append(queue_2)
queue_3 = Queue(6, 0, 1000)
queues.append(queue_3)
queue_4 = Queue(20, 0, 1000)
queues.append(queue_4)
user_0 = User(134,282)
users.append(user_0)
user_1 = User(103,235)
users.append(user_1)
user_2 = User(483,680)
users.append(user_2)
user_3 = User(174,421)
users.append(user_3)
user_4 = User(106,271)
users.append(user_4)
user_5 = User(35,163)
users.append(user_5)
user_6 = User(171,390)
users.append(user_6)
user_7 = User(465,591)
users.append(user_7)
user_8 = User(50,212)
users.append(user_8)
user_9 = User(254,395)
users.append(user_9)
user_10 = User(348,548)
users.append(user_10)
user_11 = User(416,563)
users.append(user_11)
user_12 = User(386,532)
users.append(user_12)
user_13 = User(275,386)
users.append(user_13)
user_14 = User(164,298)
users.append(user_14)
user_15 = User(70,303)
users.append(user_15)
user_16 = User(269,493)
users.append(user_16)
user_17 = User(290,427)
users.append(user_17)
user_18 = User(418,546)
users.append(user_18)
user_19 = User(314,418)
users.append(user_19)
user_20 = User(44,170)
users.append(user_20)
user_0_request_0 = QueueRequest(user_0, queue_3, 134, 282)
user_1_request_0 = QueueRequest(user_1, queue_2, 103, 235)
user_2_request_0 = QueueRequest(user_2, queue_1, 483, 680)
user_3_request_0 = QueueRequest(user_3, queue_0, 174, 421)
user_3_request_1 = QueueRequest(user_3, queue_4, 174, 421)
user_4_request_0 = QueueRequest(user_4, queue_3, 106, 271)
user_5_request_0 = QueueRequest(user_5, queue_2, 35, 163)
user_6_request_0 = QueueRequest(user_6, queue_1, 171, 390)
user_7_request_0 = QueueRequest(user_7, queue_0, 465, 591)
user_7_request_1 = QueueRequest(user_7, queue_4, 465, 591)
user_8_request_0 = QueueRequest(user_8, queue_3, 50, 212)
user_9_request_0 = QueueRequest(user_9, queue_2, 254, 395)
user_10_request_0 = QueueRequest(user_10, queue_1, 348, 548)
user_11_request_0 = QueueRequest(user_11, queue_0, 416, 563)
user_11_request_1 = QueueRequest(user_11, queue_4, 416, 563)
user_12_request_0 = QueueRequest(user_12, queue_3, 386, 532)
user_13_request_0 = QueueRequest(user_13, queue_2, 275, 386)
user_14_request_0 = QueueRequest(user_14, queue_1, 164, 298)
user_15_request_0 = QueueRequest(user_15, queue_0, 70, 303)
user_15_request_1 = QueueRequest(user_15, queue_4, 70, 303)
user_16_request_0 = QueueRequest(user_16, queue_3, 269, 493)
user_17_request_0 = QueueRequest(user_17, queue_2, 290, 427)
user_18_request_0 = QueueRequest(user_18, queue_1, 418, 546)
user_19_request_0 = QueueRequest(user_19, queue_0, 314, 418)
user_19_request_1 = QueueRequest(user_19, queue_4, 314, 418)
user_20_request_0 = QueueRequest(user_20, queue_3, 44, 170)
problem_data = ProblemData(queues, users, 'Random Intervals')

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

# if you want to replay the scenario (and change it), you can print the code used for it
# (this is why we don't just pickle)
# problem_data.gen_code()

if problem_data.check_feasibility() == True:
    print("Additional Feasibility Check passed")
else:
    raise Exception("Problem is not feasible")