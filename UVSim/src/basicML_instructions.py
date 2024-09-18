# Instruction Set: Define the functions for each BasicML instruction (READ, WRITE, LOAD, etc.). Each function will interact with the memory and accumulator.
#Maybe get rid of this 
def handle_read(self, address):
    value = int(input("Enter a value: "))
    self.memory.set_value(address, value)

def handle_write(self, address):
    value = self.memory.get_value(address)
    print(f"Output: {value}")

def handle_load(self, address):
    value = self.memory.get_value(address)
    self.accumulator.value = value

def handle_add(self, address):
    print("ADD function")

def handle_subtract(self, address):
    print("SUBTRACT function")

def handle_divide(self, address):
    print("DIVIDE function")

def handle_multiply(self, address):
    print("MULTIPLY function")

def handle_branch(self, address):
    print("BRANCH function")

def handle_branchNeg(self, address):
    print("BRANCHNEG function")
def handle_branchZero(self, address):
    print("branchZERO function")
def handle_halt(self, address):
    print("HALT function")