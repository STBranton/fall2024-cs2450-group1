# Command-line interface: When starting the program, ask the user to provide a file path for the BasicML program.
if __name__ == "__main__":
    file_path = input("Enter the program file path: ")
    program = load_program_from_file(file_path)

    memory = Memory()
    memory.load_program(program)
    
    accumulator = Accumulator()
    cpu = CPU(memory, accumulator)

    while True:
        cpu.execute_instruction()
