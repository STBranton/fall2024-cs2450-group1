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
        # Add remaining instructions here
        
        self.instruction_counter += 1  # Move to the next instruction