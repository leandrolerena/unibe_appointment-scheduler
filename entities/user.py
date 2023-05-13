from random import random
from typing import Self
import random


MAX_INT = 2 ** 32 - 1


class User:
    def __init__(self, earliest: int = 0, latest: int = MAX_INT):
        self.earliest = earliest
        self.latest = latest


    @classmethod
    def random(cls) -> Self:
        earliest = random.randint(0, 500)
        latest = earliest + random.randint(200, 500)
        return User(earliest, latest)
