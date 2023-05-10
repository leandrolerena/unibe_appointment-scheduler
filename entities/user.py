MAX_INT = 2 ** 32 - 1


class User:
    def __init__(self, earliest: int = 0, latest: int = MAX_INT):
        self.earliest = earliest
        self.latest = latest

