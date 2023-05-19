from typing import List

from entities.requesting import Queue, User


class ProblemData:
    def __init__(self, queues: List[Queue], users: List[User]):
        self.queues = queues
        self.users = users

    def process(self):
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
