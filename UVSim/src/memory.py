# Memory Management (100-word memory), this represents the UVSim's memory

class Memory:
    def __init__(self, max_size):
        self.max_size = max_size
        self.memory = [0] * self.max_size

    def load_program(self, program):
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
        return self.memory[address]

    def set_value(self, address, value):
        self.memory[address] = value
