import random
from typing import Self


class Queue:
    def __init__(self, time_serving: int = 10):
        self.time_serving = time_serving

    @classmethod
    def random(cls) -> Self:
        serving_time = random.randint(5, 30)
        return Queue(serving_time)
