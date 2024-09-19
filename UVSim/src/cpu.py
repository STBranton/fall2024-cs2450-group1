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
        print(f"{value}")

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
        match opcode:
            case 10:
                self.handle_read(operand)
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
            case 41:
                self.handle_branchNeg(operand)
            case 42:
                self.handle_branchZero(operand)
            case 43:
                self.handle_halt(operand)
            case default:
                print("Invalid Instruction, please edit")
        

        self.instruction_counter += 1  # Move to the next instruction 