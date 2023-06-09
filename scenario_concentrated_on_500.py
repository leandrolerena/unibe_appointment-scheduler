import os
from typing import List

from entities.problem_data import ProblemData
from entities.requesting import Queue, User, QueueRequest
from plotting.plot_queue_perspective import PlotQueuePerspective
from plotting.plot_user_perspective import PlotUserPerspective
from problems.appointment_multistation import AppointmentMultiStation


queues: List[Queue] = []
users: List[User] = []
queue_0 = Queue(8, 0, 1000)
queues.append(queue_0)
queue_1 = Queue(25, 0, 1000)
queues.append(queue_1)
queue_2 = Queue(29, 0, 1000)
queues.append(queue_2)
queue_3 = Queue(18, 0, 1000)
queues.append(queue_3)
queue_4 = Queue(21, 0, 1000)
queues.append(queue_4)
user_0 = User(500,500)
users.append(user_0)
user_1 = User(500,500)
users.append(user_1)
user_2 = User(500,500)
users.append(user_2)
user_3 = User(500,500)
users.append(user_3)
user_4 = User(500,500)
users.append(user_4)
user_5 = User(500,500)
users.append(user_5)
user_6 = User(500,500)
users.append(user_6)
user_7 = User(500,500)
users.append(user_7)
user_8 = User(500,500)
users.append(user_8)
user_9 = User(500,500)
users.append(user_9)
user_10 = User(500,500)
users.append(user_10)
user_11 = User(500,500)
users.append(user_11)
user_12 = User(500,500)
users.append(user_12)
user_13 = User(500,500)
users.append(user_13)
user_14 = User(500,500)
users.append(user_14)
user_15 = User(500,500)
users.append(user_15)
user_16 = User(500,500)
users.append(user_16)
user_17 = User(500,500)
users.append(user_17)
user_18 = User(500,500)
users.append(user_18)
user_19 = User(500,500)
users.append(user_19)
user_20 = User(500,500)
users.append(user_20)
user_0_request_0 = QueueRequest(user_0, queue_3, 500, 500)
user_1_request_0 = QueueRequest(user_1, queue_2, 500, 500)
user_2_request_0 = QueueRequest(user_2, queue_1, 500, 500)
user_3_request_0 = QueueRequest(user_3, queue_0, 500, 500)
user_3_request_1 = QueueRequest(user_3, queue_4, 500, 500)
user_4_request_0 = QueueRequest(user_4, queue_3, 500, 500)
user_5_request_0 = QueueRequest(user_5, queue_2, 500, 500)
user_6_request_0 = QueueRequest(user_6, queue_1, 500, 500)
user_7_request_0 = QueueRequest(user_7, queue_0, 500, 500)
user_7_request_1 = QueueRequest(user_7, queue_4, 500, 500)
user_8_request_0 = QueueRequest(user_8, queue_3, 500, 500)
user_9_request_0 = QueueRequest(user_9, queue_2, 500, 500)
user_10_request_0 = QueueRequest(user_10, queue_1, 500, 500)
user_11_request_0 = QueueRequest(user_11, queue_0, 500, 500)
user_11_request_1 = QueueRequest(user_11, queue_4, 500, 500)
user_12_request_0 = QueueRequest(user_12, queue_3, 500, 500)
user_13_request_0 = QueueRequest(user_13, queue_2, 500, 500)
user_14_request_0 = QueueRequest(user_14, queue_1, 500, 500)
user_15_request_0 = QueueRequest(user_15, queue_0, 500, 500)
user_15_request_1 = QueueRequest(user_15, queue_4, 500, 500)
user_16_request_0 = QueueRequest(user_16, queue_3, 500, 500)
user_17_request_0 = QueueRequest(user_17, queue_2, 500, 500)
user_18_request_0 = QueueRequest(user_18, queue_1, 500, 500)
user_19_request_0 = QueueRequest(user_19, queue_0, 500, 500)
user_19_request_1 = QueueRequest(user_19, queue_4, 500, 500)
user_20_request_0 = QueueRequest(user_20, queue_3, 500, 500)
problem_data = ProblemData(queues, users, 'Concentrated on 500')

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