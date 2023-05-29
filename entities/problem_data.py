from typing import List

from entities.requesting import Queue, User


class ProblemData:
    def __init__(self, queues: List[Queue], users: List[User], scenario_name: str = None):
        self.queues = queues
        self.users = users
        self.scenario_name = scenario_name
        self.solution_time = None
        self.solution_cost = None

        if self.scenario_name is None:
            self.scenario_name = f"{len(self.queues)} Queues/{len(self.users)} Users"

    def process(self):
        print("Filter out users and queues with no requests")

        self.queues = [queue for queue in self.queues if len(queue.requests) > 0]
        self.users = [user for user in self.users if len(user.requests) > 0]

        print("Determine indexes on queue for requests")

        for k in range(len(self.queues)):
            queue = self.queues[k]
            queue.index = k
            for request in queue.requests:
                request.queue_index = k
            for j in range(len(queue.requests)):
                queue.requests[j].index_on_queue = j

        print("Determine indexes on users for requests")

        for i in range(len(self.users)):
            user = self.users[i]
            user.index = i
            for request in user.requests:
                request.user_index = i
            for j in range(len(user.requests)):
                user.requests[j].index_on_user = j

        print("Determine Queue Index Mapping for User")
        for queue in self.queues:
            for request in queue.requests:
                request.user.queue_index[queue.index] = request.index_on_queue

        print("Determine User Index Mapping for Queue")
        for user in self.users:
            for request in user.requests:
                request.queue.user_index[user.index] = request.index_on_user

    def gen_code(self):
        print("Code for the scenario")

        print(f"queues: List[Queue] = []")
        print(f"users: List[User] = []")
        for queue in self.queues:
            print(f"queue_{queue.index} = Queue({queue.time_serving}, {queue.opening}, {queue.closing})")
            print(f"queues.append(queue_{queue.index})")

        for user in self.users:
            print(f"user_{user.index} = User({user.earliest},{user.latest})")
            print(f"users.append(user_{user.index})")

        for user in self.users:
            for request in user.requests:
                print(f"user_{user.index}_request_{request.index_on_user} = QueueRequest(user_{request.user.index}, "
                      f"queue_{request.queue.index}, {request.earliest}, {request.latest})")

        print(f"problem_data = ProblemData(queues, users, '{self.scenario_name}')")

    def check_feasibility(self) -> bool:
        for user in self.users:
            request_time_sorted = sorted(user.requests, key=lambda req: req.optimal_visiting_time)
            for j in range(len(request_time_sorted) - 1):
                first = request_time_sorted[j]
                second = request_time_sorted[j + 1]
                if first.optimal_visiting_time + first.visiting_duration > second.optimal_visiting_time + 0.02:
                    print(f"{first.optimal_visiting_time} + {first.visiting_duration} > {second.optimal_visiting_time}")
                    return False

        for queue in self.queues:
            request_time_sorted = sorted(queue.requests, key=lambda req: req.optimal_visiting_time)
            for j in range(len(request_time_sorted) - 1):
                first = request_time_sorted[j]
                second = request_time_sorted[j + 1]
                if first.optimal_visiting_time + first.visiting_duration > second.optimal_visiting_time + 0.02:
                    print(f"{first.optimal_visiting_time} + {first.visiting_duration} > {second.optimal_visiting_time}")
                    return False

        return True
