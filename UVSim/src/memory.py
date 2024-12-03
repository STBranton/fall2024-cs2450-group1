"""
Memory Management (100-word memory), this represents the UVSim's memory
"""

class Memory:
    """
    Represents the memory for a machine code simulator.
    Attributes:
        max_size (int): The maximum number of memory addresses available.
        memory (list): A list of integers representing the memory values.
    """
    def __init__(self, max_size):
        """
        Initializes the memory with a specified size.

        Args:
            max_size (int): The total number of memory slots available.
        """
        self.max_size = max_size
        self.memory = [0] * self.max_size

    def load_program(self, program):
        """
        Loads a program into memory, ensuring instruction formatting and size consistency.

        Args:
            program (list of str): A list of program instructions to load. Each instruction
                must be either 4 or 6 digits, optionally prefixed with '+' or '-'.

        Raises:
            ValueError: If the instructions are not consistent or not properly formatted.
        """
        length = 0
        for i, instruction in enumerate(program):
            if instruction.startswith(("+", "-")):
                core_instruction = instruction[1:]
            else:
                core_instruction = instruction
            if i == 0:
                length = len(core_instruction)

            if length != len(core_instruction):
                raise ValueError("Program instructions must all be the same length")

            if len(core_instruction) not in {4, 6}:
                raise ValueError("Program instructions must be either 4 or 6 digits (with optional '+' or '-' sign).")

            if len(core_instruction) == 4:
                core_instruction = "0" + core_instruction[:2] + "0" + core_instruction[2:]

            signed_instruction = instruction[0] + core_instruction if instruction[0] in "+-" else core_instruction
            self.memory[i] = int(signed_instruction)

    def get_value(self, address):
        """
        Retrieves the value stored at a specific memory address.

        Args:
            address (int): The address to retrieve the value from.

        Returns:
            int: The value stored at the specified memory address.
        """
        return self.memory[address]

    def set_value(self, address, value):
        """
        Stores a value at a specific memory address.

        Args:
            address (int): The address to store the value at.
            value (int): The value to store in memory.
        """
        self.memory[address] = value
