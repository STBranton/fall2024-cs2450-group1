# Implement unit tests for each component (memory, CPU, instruction execution) to ensure functionality remains consistent.
import unittest
from unittest.mock import patch
from unittest import TestCase
import os
import sys
current_dir = os.path.dirname(__file__)

src_dir = os.path.abspath(os.path.join(current_dir, '../src'))
sys.path.insert(0, src_dir)
from memory import Memory # type: ignore
from file_loader import load_program_from_file


class unitTests(unittest.TestCase):
    def test_memory_store_and_retrieve(self):
        memory = Memory()
        memory.set_value(10, 1234)
        self.assertEqual(memory.get_value(10), 1234)
    def test_load_basic_ML(self):
         @patch('yourmodule.get_input', return_value='UVSim\tests\Test1.txt')


    

if __name__ == "__main__":
    unittest.main()
