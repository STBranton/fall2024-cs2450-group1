"""
Accumulator Module
"""
class Accumulator:
    """
    Represents the accumulator in a machine code simulator.

    The accumulator is used to store the current working value during program execution
    and perform basic arithmetic operations.

    Attributes:
    value (int): The current value stored in the accumulator.
    """
    def __init__(self):
        """
        Initializes the accumulator with a default value of 0.
        """
        self.value = 0

    def add(self, value):
        """
        Adds a value to the accumulator's current value.

        Args:
            value (int): The value to add to the accumulator.
        """
        self.value += value

    def subtract(self, value):
        """
        Subtracts a value from the accumulator's current value.

        Args:
            value (int): The value to subtract from the accumulator.
        """
        self.value -= value
