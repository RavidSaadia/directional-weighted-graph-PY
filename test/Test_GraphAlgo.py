import copy
import unittest
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class MyTestCase(unittest.TestCase):

    def test_save_load(self):
        ga = GraphAlgo()
        ga.load_from_json('data/A5')

        g0 = copy.deepcopy(ga.get_graph())
        ga.save_to_json('data/A10')
        ga.load_from_json('data/A10')
        self.assertEqual(ga.get_graph(), g0)


if __name__ == '__main__':
    unittest.main()
