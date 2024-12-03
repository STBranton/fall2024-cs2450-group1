import asyncio

from cpu import CPU
from input_handler import CLIInputHandler
from memory import Memory


async def run_program(cpu):
    """
    Executes a program loaded into the CPU until a halt instruction or error occurs.

    Args:
        cpu: An instance of the CPU class, initialized with memory and handlers.

    Raises:
        Exception: If an error occurs during program execution, it is caught and printed.
    """
    try:
        while cpu.program_counter < cpu.memory.max_size:
            await cpu.execute_instruction()
    except Exception as e:
        print(f"Error during execution: {e}")


def main():
    """
    The main entry point for the program execution.

    - Prompts the user for a file path containing the program to execute.
    - Loads the program into memory.
    - Initializes the CPU with the loaded program and necessary handlers.
    - Executes the program in an asynchronous event loop.

    Handles:
        - Input/Output errors when loading the program file.
        - Exceptions during memory initialization and program execution.
        - Graceful interruption on a keyboard interrupt.

    Raises:
        Exception: If an unexpected error occurs during any step, it is caught and printed.
    """
    # Prompt user for the program file path
    file_path = input("Enter the program file path: ")

    # Load the program from the specified file
    with open(file_path, 'r') as file:
        program = [line.strip() for line in file.readlines()]

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
