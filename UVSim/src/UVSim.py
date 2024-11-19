
from input_handler import CLIInputHandler
from file_loader import load_program_from_file
from memory import Memory
from cpu import CPU

import asyncio

async def run_program(cpu):
    try:
        while cpu.program_counter < cpu.memory.max_size:
            await cpu.execute_instruction()
    except Exception as e:
        print(f"Error during execution: {e}")


def main():
    # Prompt user for the program file path
    file_path = input("Enter the program file path: ")

    # Load the program from the specified file
    program = load_program_from_file(file_path)

    if not program:
        print("Failed to load the program. Please check the file and try again.")
        return

    # Initialize memory and load the program
    memory = Memory(max_size=250)
    try:
        memory.load_program(program)
    except Exception as e:
        print(f"Error loading program into memory: {e}")
        return

    # Initialize the CLI input handler
    input_handler = CLIInputHandler()

    # Initialize the CPU with memory, input handler, and output callback
    cpu = CPU(memory, input_handler, output_callback=print)

    # Run the CPU execution within the asyncio event loop
    try:
        asyncio.run(run_program(cpu))
    except KeyboardInterrupt:
        print("\nProgram execution interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()