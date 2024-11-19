# The CPU class will handle program execution and instruction processing.
from accumulator import Accumulator


class CPU:
    def __init__(self, memory, input_handler, output_callback=None):
        self.memory = memory
        self.accumulator = Accumulator()
        self.program_counter = 0 # Points to the next instruction
        self.instruction_register = None # Points to the current instruction
        self.input_handler = input_handler
        self.output_callback = output_callback


    async def handle_read(self, address):
        
        self.output_callback("Awaiting user input...")
        input_value = await self.input_handler.get_input()
        try:
            int_value = int(input_value)
        except ValueError:
            raise ValueError(f"Invalid input '{input_value}'; expected an integer.")

        self.memory.set_value(address, int_value)

    def handle_write(self, address):
        
        value = self.memory.get_value(address)
        output_message = f"Output: {value}"
        self.output_callback(output_message)

    def handle_load(self, address):
        
        value = self.memory.get_value(address)
        self.accumulator.value = value

    def handle_store(self,address):
        
        value = self.accumulator.value
        self.memory.set_value(address, value)

    def handle_add(self, address):
        
        value = self.memory.get_value(address)
        self.accumulator.value = self.accumulator.value + value

    def handle_subtract(self, address):
        
        value = self.memory.get_value(address)
        self.accumulator.value = self.accumulator.value - value

    def handle_divide(self, address):
        
        value = self.memory.get_value(address)
        self.accumulator.value = self.accumulator.value / value

    def handle_multiply(self, address):
        
        value = self.memory.get_value(address)
        self.accumulator.value = self.accumulator.value * value

    def handle_branch(self, address):
        
        self.program_counter = address


    def handle_branch_neg(self, address):
        
        if self.accumulator.value < 0:
            self.program_counter = address

    def handle_branch_zero(self, address):
        
        if self.accumulator.value == 0:
            self.program_counter = address

    def handle_halt(self):
        self.program_counter = self.memory.max_size
        self.output_callback("Program finished")


    async def execute_instruction(self):
        self.instruction_register = self.memory.get_value(self.program_counter)
        opcode = self.instruction_register // 1000
        operand = self.instruction_register % 1000
        if operand >= 250:
            raise ValueError(f"Invalid address '{operand}'; expected an address space less than 250")
        match opcode:
            case 10:
                await self.handle_read(operand)
            case 11:
                self.handle_write(operand)
            case 20:
                self.handle_load(operand)
            case 21:
                self.handle_store(operand)

            #ARITHMETIC OPERATIONS ------
            case 30:
                self.handle_add(operand)
            case 31:
                self.handle_subtract(operand)
            case 32:
                self.handle_divide(operand)
            case 33:
                self.handle_multiply(operand)

            #CONTROL OPERATIONS-------
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
            case _:
                self.output_callback("Invalid Instruction, please edit")
        

        self.program_counter += 1  # Move to the next instruction