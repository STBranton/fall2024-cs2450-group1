# Implement unit tests for each component (memory, CPU, instruction execution) to ensure functionality remains consistent.
import unittest
import os
import sys
current_dir = os.path.dirname(__file__)

src_dir = os.path.abspath(os.path.join(current_dir, '../src'))
sys.path.insert(0, src_dir)
from memory import Memory # type: ignore

class TestMemory(unittest.TestCase):
    def test_memory_store_and_retrieve(self):
        memory = Memory()
        memory.set_value(10, 1234)
        self.assertEqual(memory.get_value(10), 1234)
        memory = Memory()
        memory.getvalue(10,)

if __name__ == "__main__":
    unittest.main()
