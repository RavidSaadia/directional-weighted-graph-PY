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
    for i in range(nodes):
        g0.add_node(i, (r.random() / 70, r.random() / 70))
    while edges > 0:
        l = list(g0.get_all_v().keys())
        s, e = map(r.choice, [l, l])
        edges -= g0.add_edge(s, e, r.uniform(1, 2))
    return g0


def modifySP(r, g0, start):
    if start not in g0.get_all_v():
        return None
    cur = g0.get_all_v()[start]
    res = [cur]
    ni = g0.all_out_edges_of_node(start)
    while ni and len(res) < 10:
        cur.tag = 1
        n = None
        for i in ni:
            if g0.get_all_v()[i].tag == 0:
                n = g0.get_all_v()[i]
                break
        if not n:
            return [k.id() for k in res]
        g0.remove_edge(cur.id(), n.id())
        g0.add_edge(cur.id(), n.id(), r.uniform(0, 0.1))
        cur = n
        res.append(cur)
        ni = g0.all_out_edges_of_node(cur.id())
    return [k.id() for k in res]


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
        # Graphics.paint(g0, title=f'Graph seed: {seed}')  #  if you want the title..
        ga = GraphAlgo(g0)
        ga.plot_graph()

        self.assertEqual(True, True)

    def test_shortest_path_basic(self):
        ga = GraphAlgo()
        g0 = DiGraph()
        r = rnd(x=3)
        for n_id in range(3):
            g0.add_node(n_id, (rnd.random(r) / 44, rnd.random(r) / 44))
        g0.add_edge(0, 1, 1.2)  # 0 --1.2-- 1
        g0.add_edge(0, 2, 5)  # \->5     /
        g0.add_edge(1, 2, 3)  # \      /-->3
        ga.init(g0)  # #        2
        di, path = ga.shortest_path(0, 2)

        # Graphics.paint(g0, title='test_shortest_path_basic', show_w=True)  # it's here for debug

        self.assertEqual(di, 4.2)
        self.assertEqual(path, [0, 1, 2])

    def test_shortest_path_basic2(self):
        ga = GraphAlgo()
        g0 = DiGraph()
        r = rnd(x=0)
        for n_id in range(1, 5):
            g0.add_node(n_id, (rnd.random(r) / 44, rnd.random(r) / 40))

        g0.add_edge(1, 2, 1)
        g0.add_edge(1, 4, 1)
        g0.add_edge(4, 3, 2)
        g0.add_edge(2, 3, 1)
        ga.init(g0)
        di, path = ga.shortest_path(1, 3)

        # Graphics.paint(g0, title='test_shortest_path_basic2', show_w=True)  # it's here for debug

        self.assertEqual(di, 2)
        self.assertEqual([1, 2, 3], path)

    def test_shortest_path(self):
        r = rnd(x=0)
        ga = GraphAlgo()
        for i in range(100000):
            g0 = create_graph(r.random(), 50, r.randint(0, 100))
            ga.init(g0)
            # ga.plot_graph()  # for debugging, not recommended in large loops
            start = r.randint(0, g0.v_size() - 1)
            expected = modifySP(r, g0, start)
            if not expected:
                expected = [start]
            d, SP = ga.shortest_path(start, expected[-1])
            self.assertEqual(expected, SP)


if __name__ == '__main__':
    unittest.main()
