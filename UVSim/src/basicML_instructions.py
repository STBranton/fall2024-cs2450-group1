# Instruction Set: Define the functions for each BasicML instruction (READ, WRITE, LOAD, etc.). Each function will interact with the memory and accumulator.

def handle_read(self, address):
    value = int(input("Enter a value: "))
    self.memory.set_value(address, value)

def handle_write(self, address):
    value = self.memory.get_value(address)
    print(f"Output: {value}")

def handle_load(self, address):
    value = self.memory.get_value(address)
    self.accumulator.value = value
'''
ADD = 30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).

Control operation:
BRANCH = 40 Branch to a specific location in memory
BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.
BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.
HALT = 43 Pause the program
'''