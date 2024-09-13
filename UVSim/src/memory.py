# Memory Management (100-word memory), this represents the UVSim's memory 
class Memory:
    def __init__(self):
        self.memory = [0] * 100
    
    def load_program(self, program):
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def get_value(self, address):
        return self.memory[address]

    def set_value(self, address, value):
        self.memory[address] = value
