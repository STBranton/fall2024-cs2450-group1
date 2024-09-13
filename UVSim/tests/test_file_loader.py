# Used to test inputs for file_loader.py
def load_program_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            program = [int(line.strip()) for line in file.readlines()]
        return program
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except ValueError:
        print("Error: Invalid program format. Ensure all lines are valid BasicML instructions.")
        return []
