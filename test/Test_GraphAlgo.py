import copy
import unittest

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)




    def test_save_load(self):
        g = GraphAlgo()
        g.load_from_json('data/A5')
        g.save_to_json("data/A10.json")







if __name__ == '__main__':
    unittest.main()
