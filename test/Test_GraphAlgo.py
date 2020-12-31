import copy
import unittest
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
from random import Random as rnd
import Graphics

key = -1


def get_new_key():
    global key
    key += 1
    return key


def create_graph(seed, nodes, edges):
    g0 = DiGraph()
    r = rnd(x=seed)
    for i in range(nodes):
        g0.add_node(get_new_key(), (rnd.random(r) / 44, rnd.random(r) / 40))
    while edges > 0:
        edges -= g0.add_edge(r.choice(list(g0.get_all_v().keys())), r.choice(list(g0.get_all_v().keys())), 0)
    return g0


class MyTestCase(unittest.TestCase):
    def test_save_load(self):
        ga = GraphAlgo()
        ga.load_from_json('data/A5')

        g0 = copy.deepcopy(ga.get_graph())
        ga.save_to_json('data/A10')
        ga.load_from_json('data/A10')
        self.assertEqual(ga.get_graph(), g0)

    def test_graphics(self):
        seed = rnd.randint(rnd(), 0, 100)
        print(f'showing graph with seed {seed}')
        g0 = create_graph(seed, 30, 50)
        Graphics.paint(g0,seed)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
