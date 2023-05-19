import random
from typing import Self, List, Mapping, Dict

MAX_INT = 2 ** 32 - 1


class Queue:
    def __init__(self, time_serving: int = 10, opening: int = 8 * 60, closing: int = 18 * 60):
        self.time_serving = time_serving
        self.requests: List[QueueRequest] = []
        self.index = None
        # Map from User Index to Queues Index on User
        self.user_index: Dict[int, int] = {}

    @classmethod
    def random(cls) -> Self:
        serving_time = random.randint(5, 30)
        return Queue(serving_time)

    def add_request(self, request: "QueueRequest"):
        self.requests.append(request)


class User:
    def __init__(self, earliest: int = 0, latest: int = MAX_INT):
        self.earliest = earliest
        self.latest = latest
        self.requests: List[QueueRequest] = []
        self.index = None
        # Map from Queue index to Users Index on Queue
        self.queue_index: Dict[int, int] = {}

    @classmethod
    def random(cls) -> Self:
        earliest = random.randint(0, 500)
        latest = earliest + random.randint(200, 500)
        return User(earliest, latest)

    def add_request(self, request: "QueueRequest"):
        self.requests.append(request)


class QueueRequest:
    def __init__(self, user: "User", queue: "Queue", earliest: int = None, latest: int = None):
        self.user = user
        self.queue = queue
        self.earliest = earliest if earliest else self.user.earliest
        self.latest = latest if latest else self.user.latest
        self.queue_index = None
        self.user_index = None
        self.index_on_queue = None
        self.index_on_user = None

