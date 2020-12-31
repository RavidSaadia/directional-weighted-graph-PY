import copy
import unittest
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
from random import Random as rnd
import src.Graphics as Graphics

key = -1


def get_new_key():
    global key
    key += 1
    return key


def create_graph(seed, nodes, edges):
    g0 = DiGraph()
    r = rnd(x=seed)
    for _ in range(nodes):
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
        Graphics.paint(g0, 0)

        self.assertEqual(True, True)

    def test_shortest_path_basic(self):
        ga = GraphAlgo()
        g0 = DiGraph()
        g0.add_node(0, None)
        g0.add_node(1, None)
        g0.add_node(2, None)
        g0.add_edge(0, 1, 1.2)  # 0 --1.2-- 1
        g0.add_edge(0, 2, 5)  # \->5     /
        g0.add_edge(1, 2, 3)  # \      /-->3
        ga.init(g0)  # #        2
        di, path = ga.shortest_path(0, 2)
        self.assertEqual(di, 4.2)
        self.assertEqual(path, [0, 1, 2])

    def test_shortest_path_basic2(self):
        ga = GraphAlgo()
        g0 = DiGraph()
        g0.add_node(0, None)
        g0.add_node(1, None)
        g0.add_node(2, None)
        g0.add_node(3, None)
        g0.add_node(4, None)
        g0.add_node(5, None)
        g0.add_edge(0, 1, 100)
        g0.add_edge(0, 5, 10)
        g0.add_edge(5, 2, 10)
        g0.add_edge(2, 3, 10)
        g0.add_edge(3, 4, 10)
        g0.add_edge(4, 1, 10)
        ga.init(g0)
        di, path = ga.shortest_path(0, 1)
        # Graphics.paint(g0, 5)

        self.assertEqual(di, 50)
        self.assertEqual(path, [0, 5, 2, 3, 4, 1])

    def test_shortest_path(self):
        ga = GraphAlgo()
        g0 = DiGraph()
        for n_id in range(6):
            g0.add_node(n_id, None)

        g0.add_edge(0, 1, 1.2)
        g0.add_edge(0, 2, 5)
        g0.add_edge(1, 2, 3)
        ga.init(g0)


if __name__ == '__main__':
    unittest.main()
