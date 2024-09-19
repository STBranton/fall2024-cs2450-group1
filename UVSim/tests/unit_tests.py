# Implement unit tests for each component (memory, CPU, instruction execution) to ensure functionality remains consistent.
import unittest
from unittest.mock import patch
from unittest import TestCase
import os
import sys
import io
current_dir = os.path.dirname(__file__)

src_dir = os.path.abspath(os.path.join(current_dir, '../src'))
sys.path.insert(0, src_dir)
from memory import Memory # type: ignore
from file_loader import load_program_from_file # type: ignore
from accumulator import Accumulator # type: ignore
from cpu import CPU # type: ignore


class unitTests(unittest.TestCase):
    def test_memory_store_and_retrieve1(self):
        memory = Memory()
        memory.set_value(10, 1234)
        self.assertEqual(memory.get_value(10), 1234)
    def test_memory_store_and_retrieve2(self):
        memory = Memory()
        memory.set_value(11, 567)
        memory.get_value(11)
        self.assertEqual(memory.get_value(11), 567)
    def test_load_basic_ml_Test1(self):
        file_path = 'UVSim/tests/Test1.txt'
        with patch('builtins.input', return_value=file_path):
            this_program = load_program_from_file(file_path)
            self.assertTrue(this_program)
    def test_load_basic_ml_Test2(self):
        file_path = 'UVSim/tests/Test2.txt'
        with patch('builtins.input', return_value=file_path):
            this_program = load_program_from_file(file_path)
            self.assertTrue(this_program)
    def test_read1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 87
        valueGave = 5
        with patch('builtins.input', return_value=valueGave):
            cpu.handle_read(address)
            newValue = cpu.memory.memory[address]
            self.assertEqual(newValue, valueGave)
    def test_read2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 85
        valueGave = 10
        with patch('builtins.input', return_value=valueGave):
            cpu.handle_read(address)
            newValue = cpu.memory.memory[address]
            self.assertEqual(newValue, valueGave)
    def test_write1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 85
        value = 1005
        cpu.memory.memory[address] = value
        captured_word = io.StringIO()
        with patch('sys.stdout', new=captured_word):
            cpu.handle_write(address)
        printed_value = captured_word.getvalue()
        self.assertEqual(value, int(printed_value.strip()))
    def test_write2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 67
        value = 9007
        cpu.memory.memory[address] = value
        captured_word = io.StringIO()
        with patch('sys.stdout', new=captured_word):
            cpu.handle_write(address)
        printed_value = captured_word.getvalue()
        self.assertEqual(value, int(printed_value.strip()))
    def test_load1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 67
        value = 567
        cpu.memory.memory[address] = value
        cpu.handle_load(address)
        self.assertEqual(accumulator.value, value)
    def test_load2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 45
        value = 100085
        cpu.memory.memory[address] = value
        cpu.handle_load(address)
        self.assertEqual(accumulator.value, value)
    def test_store1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 45
        original_value = 100085
        accumulator.value = original_value
        cpu.handle_store(address)
        new_value = cpu.memory.memory[address]
        self.assertEqual(new_value, original_value)
    def test_store2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 31
        original_value = 10078
        accumulator.value = original_value
        cpu.handle_store(address)
        new_value = cpu.memory.memory[address]
        self.assertEqual(new_value, original_value)
    def test_add1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 31
        original_accumulator_value= 10078
        original_address_value = 76
        cpu.memory.memory[address] = original_address_value
        accumulator.value = original_accumulator_value
        cpu.handle_add(address)
        values_added = original_address_value + original_accumulator_value
        self.assertEqual(values_added, accumulator.value)
    def test_add2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 56
        original_accumulator_value= 10045
        original_address_value = 1234
        cpu.memory.memory[address] = original_address_value
        accumulator.value = original_accumulator_value
        cpu.handle_add(address)
        values_added = original_address_value + original_accumulator_value
        self.assertEqual(values_added, accumulator.value)
    def test_subtract1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 56
        original_accumulator_value= 10045
        original_address_value = 1234
        cpu.memory.memory[address] = original_address_value
        accumulator.value = original_accumulator_value
        cpu.handle_subtract(address)
        values_subtracted = original_accumulator_value - original_address_value
        self.assertEqual(values_subtracted, accumulator.value)
    def test_subtract2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 87
        original_accumulator_value= 132487
        original_address_value = 584
        cpu.memory.memory[address] = original_address_value
        accumulator.value = original_accumulator_value
        cpu.handle_subtract(address)
        values_subtracted = original_accumulator_value - original_address_value
        self.assertEqual(values_subtracted, accumulator.value)
    def test_divide1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 56
        original_accumulator_value= 10045
        original_address_value = 1234
        cpu.memory.memory[address] = original_address_value
        accumulator.value = original_accumulator_value
        cpu.handle_divide(address)
        values_divded = original_accumulator_value / original_address_value
        self.assertEqual(values_divded, accumulator.value)
    def test_divide2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 56
        original_accumulator_value= 1000
        original_address_value = 10
        cpu.memory.memory[address] = original_address_value
        accumulator.value = original_accumulator_value
        cpu.handle_divide(address)
        values_divded = original_accumulator_value / original_address_value
        self.assertEqual(values_divded, accumulator.value)
    def test_multiply1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 56
        original_accumulator_value= 1000
        original_address_value = 10
        cpu.memory.memory[address] = original_address_value
        accumulator.value = original_accumulator_value
        cpu.handle_multiply(address)
        values_multiplied = original_accumulator_value * original_address_value
        self.assertEqual(values_multiplied, accumulator.value)
    def test_multiply2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address = 56
        original_accumulator_value= 876
        original_address_value = 2
        cpu.memory.memory[address] = original_address_value
        accumulator.value = original_accumulator_value
        cpu.handle_multiply(address)
        values_multiplied = original_accumulator_value * original_address_value
        self.assertEqual(values_multiplied, accumulator.value)
    def test_branch1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        addresss_to_branch = 87
        original_address = 99
        cpu.handle_branch(addresss_to_branch)
        self.assertEqual(cpu.instruction_counter, addresss_to_branch)
    def test_branch2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        addresss_to_branch = 45
        original_address = 34
        cpu.handle_branch(addresss_to_branch)
        self.assertEqual(cpu.instruction_counter, addresss_to_branch)
    def test_branch_neg1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        accumulator.value = -5
        addresss_to_branch = 45
        original_address = 34
        cpu.handle_branchNeg(addresss_to_branch)
        self.assertEqual(cpu.instruction_counter, addresss_to_branch)
    def test_branch_neg2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        accumulator.value = 10
        addresss_to_branch = 45
        original_address = 34
        cpu.handle_branchNeg(addresss_to_branch)
        self.assertNotEqual(cpu.instruction_counter, addresss_to_branch)
    def test_branch_zero1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        accumulator.value = 10
        addresss_to_branch = 45
        original_address = 34
        cpu.handle_branchZero(addresss_to_branch)
        self.assertNotEqual(cpu.instruction_counter, addresss_to_branch)
    def test_branch_zero2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        accumulator.value = 0
        addresss_to_branch = 56
        original_address = 32
        cpu.handle_branchZero(addresss_to_branch)
        self.assertEqual(cpu.instruction_counter, addresss_to_branch)
    def test_halt1(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address= 98
        cpu.handle_halt(address)
        cpu.instruction_counter = 100
    def test_halt2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        address= 15
        cpu.handle_halt(address)
        cpu.instruction_counter = 100
    def test_invalid_instrction(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        captured_word = io.StringIO()
        instruction = 12341234123412
        cpu.memory.memory[0] = instruction
        with patch('sys.stdout', new=captured_word):
            cpu.execute_instruction()
        printed_value = captured_word.getvalue()
        self.assertEqual("Invalid Instruction, please edit", printed_value.strip())
    def test_invalid_instrction2(self):
        accumulator = Accumulator()
        memory = Memory()
        cpu = CPU(memory, accumulator)
        captured_word = io.StringIO()
        instruction = -12341234673412
        cpu.memory.memory[0] = instruction
        with patch('sys.stdout', new=captured_word):
            cpu.execute_instruction()
        printed_value = captured_word.getvalue()
        self.assertEqual("Invalid Instruction, please edit", printed_value.strip())















    

if __name__ == "__main__":
    unittest.main()
