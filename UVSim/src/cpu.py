# The CPU class will handle program execution and instruction processing.
class CPU:
    def __init__(self, memory, accumulator):
        self.memory = memory
        self.accumulator = accumulator
        self.instruction_counter = 0  # Points to the current instruction
        
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
        elif opcode == 31: # STORE:
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
            self.handle_branchneg(operand)
        elif opcode == 42: #BRANCHZERO
            self.handle_branchZero(operand)
        elif opcode == 43: #HALT
            self.handle_halt(operand)

        
        self.instruction_counter += 1  # Move to the next instruction