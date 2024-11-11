# Implement unit tests for each component (memory, CPU, instruction execution) to ensure functionality remains consistent.
import io
import os
import sys
import unittest
from pathlib import Path
from unittest.async_case import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock

from UVSim.src.input_handler import CLIInputHandler

current_dir = os.path.dirname(__file__)

src_dir = os.path.abspath(os.path.join(current_dir, '../src'))
sys.path.insert(0, src_dir)
from memory import Memory  # type: ignore
from file_loader import load_program_from_file  # type: ignore
from accumulator import Accumulator  # type: ignore
from cpu import CPU  # type: ignore


class unitTests(IsolatedAsyncioTestCase):
    def test_memory_store_and_retrieve1(self):
        memory = Memory(250)
        memory.set_value(10, 1234)
        self.assertEqual(memory.get_value(10), 1234)

    def test_memory_store_and_retrieve2(self):
        memory = Memory(250)
        memory.set_value(11, 567)
        memory.get_value(11)
        self.assertEqual(memory.get_value(11), 567)

    def test_load_basic_ml_Test1(self):
        file_path = Path(__file__).parent / "Test1.txt"
        memory = Memory(250)
        cpu = CPU(memory, input_handler=CLIInputHandler, output_callback=print)
        program = load_program_from_file(file_path)
        with self.assertRaises(ValueError) as context:
                    cpu.memory.load_program(program)
        self.assertEqual(str(context.exception), "Program instructions must all be the same length")

    def test_load_basic_ml_Test2(self):
        file_path = Path(__file__).parent / "Test2.txt"
        memory = Memory(250)
        cpu = CPU(memory, input_handler=CLIInputHandler, output_callback=print)
        program = load_program_from_file(file_path)
        cpu.memory.load_program(program)

    def test_load_invalid_length_command(self):
        file_path = Path(__file__).parent / "Test3.txt"
        memory = Memory(250)
        cpu = CPU(memory, input_handler=CLIInputHandler, output_callback=print)
        program = load_program_from_file(file_path)
        with self.assertRaises(ValueError) as context:
            cpu.memory.load_program(program)
        self.assertEqual(str(context.exception), "Program instructions must be either 4 or 6 digits (with optional '+' or '-' sign).")

    async def test_read(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "010200"
        memory.load_program([instruction])
        address = 200
        valueGave = 5
        with patch('builtins.input', return_value=valueGave):
            await cpu.execute_instruction()
            newValue = cpu.memory.memory[address]
            self.assertEqual(newValue, valueGave)

    async def test_invalid_read(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "010085"
        memory.load_program([instruction])
        return_value = "BOOM!"
        with patch.object(input_handler, 'get_input', AsyncMock(return_value=return_value)):
            with self.assertRaises(ValueError) as context:
                await cpu.execute_instruction()

            self.assertEqual(str(context.exception), f"Invalid input '{return_value}'; expected an integer.")

    async def test_write1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "011085"
        memory.load_program([instruction])
        address = 85
        value = 1005
        cpu.memory.memory[address] = value
        captured_word = io.StringIO()
        with patch('sys.stdout', new=captured_word):
            await cpu.execute_instruction()
        printed_value = int(captured_word.getvalue().replace("Output: ", "").strip())
        self.assertEqual(value, printed_value)

    async def test_write2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "011067"
        memory.load_program([instruction])
        address = 67
        value = 9007
        cpu.memory.memory[address] = value
        captured_word = io.StringIO()
        with patch('sys.stdout', new=captured_word):
            await cpu.execute_instruction()
        printed_value = int(captured_word.getvalue().replace("Output: ", "").strip())
        self.assertEqual(value, printed_value)

    async def test_load1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "020067"
        memory.load_program([instruction])
        address = 67
        value = 567
        cpu.memory.memory[address] = value
        await cpu.execute_instruction()
        self.assertEqual(cpu.accumulator.value, value)

    async def test_load2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "020045"
        memory.load_program([instruction])
        address = 45
        value = 100085
        cpu.memory.memory[address] = value
        await cpu.execute_instruction()
        self.assertEqual(cpu.accumulator.value, value)

    async def test_store1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "021045"
        memory.load_program([instruction])
        address = 45
        original_value = 100085
        cpu.accumulator.value = original_value
        await cpu.execute_instruction()
        new_value = cpu.memory.memory[address]
        self.assertEqual(new_value, original_value)

    async def test_store2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "021031"
        memory.load_program([instruction])
        address = 31
        original_value = 10078
        cpu.accumulator.value = original_value
        await cpu.execute_instruction()
        new_value = cpu.memory.memory[address]
        self.assertEqual(new_value, original_value)

    async def test_add1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "030031"
        memory.load_program([instruction])
        address = 31
        original_accumulator_value = 10078
        original_address_value = 76
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        await cpu.execute_instruction()
        values_added = original_address_value + original_accumulator_value
        self.assertEqual(values_added, cpu.accumulator.value)

    async def test_add2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "030056"
        memory.load_program([instruction])
        address = 56
        original_accumulator_value = 10045
        original_address_value = 1234
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        await cpu.execute_instruction()
        values_added = original_address_value + original_accumulator_value
        self.assertEqual(values_added, cpu.accumulator.value)

    async def test_subtract1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "031056"
        memory.load_program([instruction])
        address = 56
        original_accumulator_value = 10045
        original_address_value = 1234
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        await cpu.execute_instruction()
        values_subtracted = original_accumulator_value - original_address_value
        self.assertEqual(values_subtracted, cpu.accumulator.value)

    async def test_subtract2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "031087"
        memory.load_program([instruction])
        address = 87
        original_accumulator_value = 132487
        original_address_value = 584
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        await cpu.execute_instruction()
        values_subtracted = original_accumulator_value - original_address_value
        self.assertEqual(values_subtracted, cpu.accumulator.value)

    async def test_divide1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "032056"
        memory.load_program([instruction])
        address = 56
        original_accumulator_value = 10045
        original_address_value = 1234
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        await cpu.execute_instruction()
        values_divided = original_accumulator_value / original_address_value
        self.assertEqual(values_divided, cpu.accumulator.value)

    async def test_divide2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "032056"
        memory.load_program([instruction])
        address = 56
        original_accumulator_value = 1000
        original_address_value = 10
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        await cpu.execute_instruction()
        values_divided = original_accumulator_value / original_address_value
        self.assertEqual(values_divided, cpu.accumulator.value)

    async def test_multiply1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "033056"
        memory.load_program([instruction])
        address = 56
        original_accumulator_value = 1000
        original_address_value = 10
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        await cpu.execute_instruction()
        values_multiplied = original_accumulator_value * original_address_value
        self.assertEqual(values_multiplied, cpu.accumulator.value)

    async def test_multiply2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "033056"
        memory.load_program([instruction])
        address = 56
        original_accumulator_value = 876
        original_address_value = 2
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        await cpu.execute_instruction()
        values_multiplied = original_accumulator_value * original_address_value
        self.assertEqual(values_multiplied, cpu.accumulator.value)

    async def test_branch1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "040087"
        memory.load_program([instruction])
        address_to_branch = 87
        await cpu.execute_instruction()
        self.assertEqual(cpu.program_counter, address_to_branch)

    async def test_branch2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "040045"
        memory.load_program([instruction])
        address_to_branch = 45
        await cpu.execute_instruction()
        self.assertEqual(cpu.program_counter, address_to_branch)

    async def test_branch_neg1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "041045"
        memory.load_program([instruction])
        cpu.accumulator.value = -5
        address_to_branch = 45
        await cpu.execute_instruction()
        self.assertEqual(cpu.program_counter, address_to_branch)

    async def test_branch_neg2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "041045"
        memory.load_program([instruction])
        cpu.accumulator.value = 10
        address_to_branch = 45
        await cpu.execute_instruction()
        self.assertNotEqual(cpu.program_counter, address_to_branch)

    async def test_branch_zero1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "042045"
        memory.load_program([instruction])
        cpu.accumulator.value = 10
        address_to_branch = 45
        await cpu.execute_instruction()
        self.assertNotEqual(cpu.program_counter, address_to_branch)

    async def test_branch_zero2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "042056"
        memory.load_program([instruction])
        cpu.accumulator.value = 0
        address_to_branch = 56
        await cpu.execute_instruction()
        self.assertEqual(cpu.program_counter, address_to_branch)

    async def test_halt1(self):
        memory_size = 250
        memory = Memory(memory_size)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "043000"
        memory.load_program([instruction])
        await cpu.execute_instruction()
        self.assertEqual(cpu.program_counter, memory_size)

    async def test_halt2(self):
        memory_size = 250
        memory = Memory(memory_size)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "043203"
        memory.load_program([instruction])
        cpu.handle_halt()
        self.assertEqual(cpu.program_counter, memory_size)

    async def test_invalid_instruction(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = 8657
        cpu.memory.memory[0] = instruction
        with self.assertRaises(Exception) as context:
            await cpu.execute_instruction()
        self.assertEqual(str(context.exception), "Invalid Instruction, please edit")

    async def test_invalid_instruction2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = -8557
        cpu.memory.memory[0] = instruction
        with self.assertRaises(Exception) as context:
            await cpu.execute_instruction()
        self.assertEqual(str(context.exception), "Invalid Instruction, please edit")

    async def test_invalid_memory_address(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        instruction = "030256"
        address = 256
        memory.load_program([instruction])
        with self.assertRaises(ValueError) as context:
            await cpu.execute_instruction()
        self.assertEqual(str(context.exception), f"Invalid address '{address}'; expected an address space less than 250")