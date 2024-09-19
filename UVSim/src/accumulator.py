# The Accumulator will store the current working value during program execution.
class Accumulator:
    def __init__(self):
        self.value = 0

    def add(self, value):
        self.value += value

    def subtract(self, value):
        self.value -= value