# The CPU class will handle program execution and instruction processing.
import basicML_instructions
class CPU:
    def __init__(self, memory, accumulator):
        self.memory = memory
        self.accumulator = accumulator
        self.instruction_counter = 0  # Points to the current instruction
    def handle_read(self, address):
        value = int(input("Enter a value: "))
        self.memory.set_value(address,value)

    def handle_write(self, address):
        value = self.memory.get_value(address)
        print(f"Output: {value}")

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
        self.instruction_counter = address



    def handle_branchNeg(self, address):
        if self.accumulator.value < 0:
            self.instruction_counter = address

    def handle_branchZero(self, address):
        if self.accumulator.value == 0:
            self.instruction_counter = address

    def handle_halt(self, address):
        self.instruction_counter = 100
            
    def execute_instruction(self):
        instruction = self.memory.get_value(self.instruction_counter)
        opcode = instruction // 100
        operand = instruction % 100
        if opcode == 10:  # READ
            self.handle_read(operand)
        elif opcode == 11:  # WRITE
            self.handle_write(operand)
        elif opcode == 20:  # LOAD
            self.handle_load(operand)
        elif opcode == 21: # STORE
            self.handle_store(operand)

        #ARITHMETIC OPERATIONS ------
        elif opcode == 30: #ADD
            self.handle_add(operand)
        elif opcode == 31: #SUBTRACT
            self.handle_subtract(operand)
        elif opcode == 32: #DIVIDE
            self.handle_divide(operand)
        elif opcode == 33: #MULTIPLY
            self.handle_multiply(operand)

        #CONTROL OPERATIONS-------
        elif opcode == 40: #BRANCH
            self.handle_branch(operand)
        elif opcode == 41: #BRANCHNEG
            self.handle_branchNeg(operand)
        elif opcode == 42: #BRANCHZERO
            self.handle_branchZero(operand)
        elif opcode == 43: #HALT
            self.handle_halt(operand)

        self.instruction_counter += 1  # Move to the next instruction 