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