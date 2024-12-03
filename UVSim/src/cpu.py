"""
The CPU class will handle program execution and instruction processing.
"""
from accumulator import Accumulator


class CPU:
    """
    Represents a basic CPU for executing a machine code simulator.

    Attributes:
        memory: The memory object for storing and retrieving values.
        accumulator: An accumulator object for performing arithmetic operations.
        program_counter: An integer pointing to the address of the next instruction to execute.
        instruction_register: Stores the current instruction being processed.
        input_handler: Handles asynchronous input from the user or system.
        output_callback: A callback function for handling output messages.
    """

    def __init__(self, memory, input_handler, output_callback=None):
        """
        Initializes the CPU with memory, input handler, and optional output callback.

        Args:
            memory: An object for storing and retrieving memory values.
            input_handler: An object for handling user input asynchronously.
            output_callback: A callable for outputting messages, defaults to None.
        """
        self.memory = memory
        self.accumulator = Accumulator()
        self.program_counter = 0
        self.instruction_register = None
        self.input_handler = input_handler
        self.output_callback = output_callback

    async def handle_read(self, address):
        """
        Reads input from the user asynchronously and stores it in memory.

        Args:
            address: The memory address where the input value will be stored.

        Raises:
            ValueError: If the input cannot be converted to an integer.
        """
        self.output_callback("Awaiting user input...")
        input_value = await self.input_handler.get_input()
        try:
            int_value = int(input_value)
        except ValueError:
            raise ValueError(f"Invalid input '{input_value}', expected an integer.")
        self.memory.set_value(address, int_value)

    def handle_write(self, address):
        """
        Outputs the value stored at a specific memory address.

        Args:
            address: The memory address to read the value from.
        """
        value = self.memory.get_value(address)
        output_message = f"Output: {value}"
        self.output_callback(output_message)

    def handle_load(self, address):
        """
        Loads a value from memory into the accumulator.

        Args:
            address: The memory address to load the value from.
        """
        value = self.memory.get_value(address)
        self.accumulator.value = value

    def handle_store(self, address):
        """
        Stores the value from the accumulator into memory.

        Args:
            address: The memory address to store the value.
        """
        value = self.accumulator.value
        self.memory.set_value(address, value)

    def handle_add(self, address):
        """
        Adds a value from memory to the accumulator.

        Args:
            address: The memory address to retrieve the value from.
        """
        value = self.memory.get_value(address)
        self.accumulator.add(value)

    def handle_subtract(self, address):
        """
        Subtracts a value from memory from the accumulator.

        Args:
            address: The memory address to retrieve the value from.
        """
        value = self.memory.get_value(address)
        self.accumulator.subtract(value)

    def handle_divide(self, address):
        """
        Divides the accumulator value by a value from memory.

        Args:
            address: The memory address to retrieve the divisor from.
        """
        value = self.memory.get_value(address)
        self.accumulator.value = self.accumulator.value / value

    def handle_multiply(self, address):
        """
        Multiplies the accumulator value by a value from memory.

        Args:
            address: The memory address to retrieve the multiplier from.
        """
        value = self.memory.get_value(address)
        self.accumulator.value = self.accumulator.value * value

    def handle_branch(self, address):
        """
        Sets the program counter to a specific address, effectively jumping to that instruction.

        Args:
            address: The address to set the program counter to.
        """
        self.program_counter = address

    def handle_branch_neg(self, address):
        """
        Branches to a specific address if the accumulator's value is negative.

        Args:
            address: The address to set the program counter to if the condition is met.
        """
        if self.accumulator.value < 0:
            self.program_counter = address

    def handle_branch_zero(self, address):
        """
        Branches to a specific address if the accumulator's value is zero.

        Args:
            address: The address to set the program counter to if the condition is met.
        """
        if self.accumulator.value == 0:
            self.program_counter = address

    def handle_halt(self):
        """
        Halts program execution and sets the program counter to the maximum memory address.
        """
        self.program_counter = self.memory.max_size
        self.output_callback("Program finished")

    async def execute_instruction(self):
        """
        Fetches, decodes, and executes the current instruction.

        Raises:
            ValueError: If the instruction is invalid or the operand address is out of range.
        """
        self.instruction_register = self.memory.get_value(self.program_counter)
        opcode = self.instruction_register // 1000
        operand = self.instruction_register % 1000
        if operand >= 250:
            raise (
                ValueError(f"Invalid address '{operand}'. expected an address space less than 250"))
        match opcode:
            case 10:
                await self.handle_read(operand)
            case 11:
                self.handle_write(operand)
            case 20:
                self.handle_load(operand)
            case 21:
                self.handle_store(operand)
            case 30:
                self.handle_add(operand)
            case 31:
                self.handle_subtract(operand)
            case 32:
                self.handle_divide(operand)
            case 33:
                self.handle_multiply(operand)
            case 40:
                self.handle_branch(operand)
                return
            case 41:
                self.handle_branch_neg(operand)
                return
            case 42:
                self.handle_branch_zero(operand)
                return
            case 43:
                self.handle_halt()
                return
            case _:
                raise ValueError("Invalid Instruction, please edit")
        self.program_counter += 1  # Move to the next instruction
