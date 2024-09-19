# Implement unit tests for each component (memory, CPU, instruction execution) to ensure functionality remains consistent.
import unittest
from UVSim.src.memory import Memory

class TestMemory(unittest.TestCase):
    def test_memory_store_and_retrieve(self):
        memory = Memory()
        memory.set_value(10, 1234)
        self.assertEqual(memory.get_value(10), 1234)

if __name__ == "__main__":
    unittest.main()
