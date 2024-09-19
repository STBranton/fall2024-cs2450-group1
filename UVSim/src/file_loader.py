# File Input Handling: Add functionality to **read the BasicML program from an input file**. Each line in the file will represent a four-digit BasicML instruction.
def load_program_from_file(file_path):
    with open(file_path, 'r') as file:
        program = [int(line.strip()) for line in file.readlines()]
    return program
