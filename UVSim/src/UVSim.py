# UVSim.py
from file_loader import load_program_from_file
from memory import Memory
from accumulator import Accumulator
from cpu import CPU
file_path = input("Enter the program file path: ")
program = load_program_from_file(file_path)

if program:  # Check if the program was successfully loaded
    memory = Memory()
    memory.load_program(program)
    
    accumulator = Accumulator()
    cpu = CPU(memory, accumulator)

    while cpu.instruction_counter < 100:
        cpu.execute_instruction()