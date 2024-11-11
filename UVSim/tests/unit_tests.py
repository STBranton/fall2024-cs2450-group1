# Implement unit tests for each component (memory, CPU, instruction execution) to ensure functionality remains consistent.
import io
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from UVSim.src.input_handler import CLIInputHandler

current_dir = os.path.dirname(__file__)

src_dir = os.path.abspath(os.path.join(current_dir, '../src'))
sys.path.insert(0, src_dir)
from memory import Memory  # type: ignore
from file_loader import load_program_from_file  # type: ignore
from accumulator import Accumulator  # type: ignore
from cpu import CPU  # type: ignore


class unitTests(unittest.TestCase):
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

    async def test_read1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 87
        valueGave = 5
        with patch('builtins.input', return_value=valueGave):
            await cpu.handle_read(address)
            newValue = cpu.memory.memory[address]
            self.assertEqual(newValue, valueGave)

    async def test_read2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 85
        valueGave = 10
        with patch('builtins.input', return_value=valueGave):
            await cpu.handle_read(address)
            newValue = cpu.memory.memory[address]
            self.assertEqual(newValue, valueGave)

    def test_write1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 85
        value = 1005
        cpu.memory.memory[address] = value
        captured_word = io.StringIO()
        with patch('sys.stdout', new=captured_word):
            cpu.handle_write(address)
        printed_value = int(captured_word.getvalue().replace("Output: ", "").strip())
        self.assertEqual(value, printed_value)

    def test_write2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 67
        value = 9007
        cpu.memory.memory[address] = value
        captured_word = io.StringIO()
        with patch('sys.stdout', new=captured_word):
            cpu.handle_write(address)
        printed_value = int(captured_word.getvalue().replace("Output: ", "").strip())
        self.assertEqual(value, printed_value)

    def test_load1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 67
        value = 567
        cpu.memory.memory[address] = value
        cpu.handle_load(address)
        self.assertEqual(cpu.accumulator.value, value)

    def test_load2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 45
        value = 100085
        cpu.memory.memory[address] = value
        cpu.handle_load(address)
        self.assertEqual(cpu.accumulator.value, value)

    def test_store1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 45
        original_value = 100085
        cpu.accumulator.value = original_value
        cpu.handle_store(address)
        new_value = cpu.memory.memory[address]
        self.assertEqual(new_value, original_value)

    def test_store2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 31
        original_value = 10078
        cpu.accumulator.value = original_value
        cpu.handle_store(address)
        new_value = cpu.memory.memory[address]
        self.assertEqual(new_value, original_value)

    def test_add1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 31
        original_accumulator_value = 10078
        original_address_value = 76
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        cpu.handle_add(address)
        values_added = original_address_value + original_accumulator_value
        self.assertEqual(values_added, cpu.accumulator.value)

    def test_add2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 56
        original_accumulator_value = 10045
        original_address_value = 1234
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        cpu.handle_add(address)
        values_added = original_address_value + original_accumulator_value
        self.assertEqual(values_added, cpu.accumulator.value)

    def test_subtract1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 56
        original_accumulator_value = 10045
        original_address_value = 1234
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        cpu.handle_subtract(address)
        values_subtracted = original_accumulator_value - original_address_value
        self.assertEqual(values_subtracted, cpu.accumulator.value)

    def test_subtract2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 87
        original_accumulator_value = 132487
        original_address_value = 584
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        cpu.handle_subtract(address)
        values_subtracted = original_accumulator_value - original_address_value
        self.assertEqual(values_subtracted, cpu.accumulator.value)

    def test_divide1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 56
        original_accumulator_value = 10045
        original_address_value = 1234
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        cpu.handle_divide(address)
        values_divded = original_accumulator_value / original_address_value
        self.assertEqual(values_divded, cpu.accumulator.value)

    def test_divide2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 56
        original_accumulator_value = 1000
        original_address_value = 10
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        cpu.handle_divide(address)
        values_divded = original_accumulator_value / original_address_value
        self.assertEqual(values_divded, cpu.accumulator.value)

    def test_multiply1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 56
        original_accumulator_value = 1000
        original_address_value = 10
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        cpu.handle_multiply(address)
        values_multiplied = original_accumulator_value * original_address_value
        self.assertEqual(values_multiplied, cpu.accumulator.value)

    def test_multiply2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        address = 56
        original_accumulator_value = 876
        original_address_value = 2
        cpu.memory.memory[address] = original_address_value
        cpu.accumulator.value = original_accumulator_value
        cpu.handle_multiply(address)
        values_multiplied = original_accumulator_value * original_address_value
        self.assertEqual(values_multiplied, cpu.accumulator.value)

    def test_branch1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        addresss_to_branch = 87
        original_address = 99
        cpu.handle_branch(addresss_to_branch)
        self.assertEqual(cpu.program_counter, addresss_to_branch)

    def test_branch2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        addresss_to_branch = 45
        original_address = 34
        cpu.handle_branch(addresss_to_branch)
        self.assertEqual(cpu.program_counter, addresss_to_branch)

    def test_branch_neg1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        cpu.accumulator.value = -5
        addresss_to_branch = 45
        original_address = 34
        cpu.handle_branch_neg(addresss_to_branch)
        self.assertEqual(cpu.program_counter, addresss_to_branch)

    def test_branch_neg2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        cpu.accumulator.value = 10
        addresss_to_branch = 45
        original_address = 34
        cpu.handle_branch_neg(addresss_to_branch)
        self.assertNotEqual(cpu.program_counter, addresss_to_branch)

    def test_branch_zero1(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        cpu.accumulator.value = 10
        addresss_to_branch = 45
        original_address = 34
        cpu.handle_branch_zero(addresss_to_branch)
        self.assertNotEqual(cpu.program_counter, addresss_to_branch)

    def test_branch_zero2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        cpu.accumulator.value = 0
        addresss_to_branch = 56
        original_address = 32
        cpu.handle_branch_zero(addresss_to_branch)
        self.assertEqual(cpu.program_counter, addresss_to_branch)

    def test_halt1(self):
        memory_size = 250
        memory = Memory(memory_size)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        cpu.handle_halt()
        self.assertEqual(cpu.program_counter, memory_size)

    def test_halt2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        cpu.handle_halt()
        cpu.program_counter = 100

    async def test_invalid_instrction(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        captured_word = io.StringIO()
        instruction = 8657
        cpu.memory.memory[0] = instruction
        with patch('sys.stdout', new=captured_word):
            await cpu.execute_instruction()
        printed_value = captured_word.getvalue()
        self.assertEqual("Invalid Instruction, please edit", printed_value.strip())

    async def test_invalid_instrction2(self):
        memory = Memory(250)
        input_handler = CLIInputHandler()
        cpu = CPU(memory, input_handler, output_callback=print)
        captured_word = io.StringIO()
        instruction = -8557
        cpu.memory.memory[0] = instruction
        with patch('sys.stdout', new=captured_word):
            await cpu.execute_instruction()
        printed_value = captured_word.getvalue()
        self.assertEqual("Invalid Instruction, please edit", printed_value.strip())


if __name__ == "__main__":
    unittest.main()
