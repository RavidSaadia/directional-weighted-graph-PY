import copy
import time
from pathlib import Path

import networkx as nx
import unittest
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
from random import Random as rnd
from src.Graphics import paint

key = -1
p = str(Path(__file__).parent.parent)

def maincheck_our(s):
    ga = GraphAlgo()
    t = time.time()
    ga.load_from_json(s)

    t = time.time() - t
    print('loaded:', t)
    print()

    t = time.time()
    ga.connected_components()
    t = time.time() - t
    print('sccs:', t)
    print()

    r = rnd(x=0)
    keys = list(ga.get_graph().get_all_v().keys())
    s, e = map(r.choice, [keys, keys])

    t = time.time()
    ga.connected_component(s)
    t = time.time() - t
    print('scc:', t)
    print()

    t = time.time()
    ga.shortest_path(s, e)
    t = time.time() - t
    print('sp:', t)
    print()


def graph_to_nx(g):
    ga = nx.DiGraph()

    for n in g.get_all_v():
        node = g.get_all_v()[n]
        ga.add_node(n)

        for e in node.get_outside():
            ga.add_edge(n, e)
            ga[n][e]['weight'] = g.get_edge(n, e)[0]
    return ga


def maincheck_networkX(s, keys):
    ga0 = GraphAlgo()
    ga0.load_from_json(s)
    ga = graph_to_nx(ga0.get_graph())

    t = time.time()
    list(nx.strongly_connected_components(ga))
    t = time.time() - t
    print('sccs:', t)
    print()

    s = keys.pop(0)
    e = keys.pop(0)
    t = time.time()

    nx.dijkstra_path(ga, source=s, target=e, weight=lambda x, y, z: ga[x][y]['weight'])
    t = time.time() - t
    print('sp:', t)
    print()


def get_new_key():
    global key
    key += 1
    return key


def create_graph(seed, nodes, edges):
    g0 = DiGraph()
    r = rnd(x=seed)
    for i in range(nodes):
        g0.add_node(i, (r.random() * 100, r.random() * 100))
    while edges > 0:
        keys = list(g0.get_all_v().keys())
        s, e = map(r.choice, [keys, keys])
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
        file_name = 'data/A5'
        file_name = p + '/' + file_name
        ga.load_from_json(file_name)

        g0 = copy.deepcopy(ga.get_graph())
        file_name = 'data/A10'
        file_name = p + '/' + file_name
        ga.save_to_json(file_name)
        ga.load_from_json(file_name)
        self.assertEqual(ga.get_graph(), g0)

    def test_graphics(self):
        seed = rnd.randint(rnd(), 0, 100)
        print(f'showing graph with seed {seed}')
        g0 = create_graph(seed, 15, 30)
        # paint(g0, title=f'Graph seed: {seed}')  #  if you want the title..
        ga = GraphAlgo(g0)
        ga.plot_graph()
        self.assertEqual(True, True)

    def test_shortest_path_basic(self):
        ga = GraphAlgo()
        g0 = DiGraph()
        r = rnd(x=3)
        for n_id in range(3):
            g0.add_node(n_id, (r.random() / 44, r.random() / 44))
        g0.add_edge(0, 1, 1.2)  # 0 --1.2-- 1
        g0.add_edge(0, 2, 5)  # \->5     /
        g0.add_edge(1, 2, 3)  # \      /-->3
        ga.init(g0)  # #        2
        di, path = ga.shortest_path(0, 2)

        # paint(g0, title='test_shortest_path_basic', show_w=True)  # it's here for debug

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

        # paint(g0, title='test_shortest_path_basic2', show_w=True)  # it's here for debug

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
            expected = modifySP(r, g0, start)  # 1 0-0.1 max 10 edges u->v is expected (u = start)
            if not expected:
                expected = [start]
            d, SP = ga.shortest_path(start, expected[-1])
            self.assertEqual(expected, SP)

    def test_DFS(self):
        g = create_graph(0, 6, 7)
        ga = GraphAlgo(g)
        f, res = ga.dfs(g.get_all_v())
        print(res)
        print(f)

    def test_transpose(self):
        g = create_graph(0, 6, 7)
        ga = GraphAlgo(g)
        ga.plot_graph()
        g = ga.transpose()
        paint(g, title="transposed")

    def test_connected_component(self):
        g = create_graph(2, 6, 7)
        ga = GraphAlgo(g)
        for i in [3, 4, 2, 5]:
            self.assertEqual({3, 4, 2, 5}, set(ga.connected_component(i)))
        self.assertEqual([1], ga.connected_component(1))
        self.assertEqual([0], ga.connected_component(0))
        self.assertEqual([], ga.connected_component(12))

    def test_connected_components(self):
        g = create_graph(2, 6, 7)
        ga = GraphAlgo(g)
        # paint(g, show_w=True)
        cons = ga.connected_components()
        to_set = {frozenset(c) for c in cons}
        self.assertEqual({frozenset([1]), frozenset([0]), frozenset([3, 5, 4, 2])}, to_set)

    def test_runtime(self):
        file_name = 'data/G_10_80_1.json'
        file_name = p + '/' + file_name
        print("G_10_80_1 :")
        maincheck_our(file_name)

        file_name = 'data/G_100_800_1.json'
        file_name = p + '/' + file_name
        print("G_100_800_1 :")
        maincheck_our(file_name)

        file_name = 'data/G_1000_8000_1.json'
        file_name = p + '/' + file_name
        print("G_1000_8000_1 :")
        maincheck_our(file_name)

        file_name = 'data/G_10000_80000_1.json'
        file_name = p + '/' + file_name
        print("G_10000_80000_1 :")
        maincheck_our(file_name)

        file_name = 'data/G_20000_160000_1.json'
        file_name = p + '/' + file_name
        print("G_20000_160000_1 :")
        maincheck_our(file_name)

        file_name = 'data/G_30000_240000_1.json'
        file_name = p + '/' + file_name
        print("G_30000_240000_1 :")
        maincheck_our(file_name)

    def test_runtimeNX(self):
        keys = [6, 6, 49, 97, 864, 394, 6311, 6890, 12623, 13781, 27670, 12623]
        print("G_10_80_1 :")
        file_name = 'data/G_10_80_1.json'
        file_name = p + '/' + file_name
        maincheck_networkX(file_name, keys)

        print("G_100_800_1 :")
        file_name = 'data/G_100_800_1.json'
        file_name = p + '/' + file_name
        maincheck_networkX(file_name, keys)

        print("G_1000_8000_1 :")
        file_name = 'data/G_1000_8000_1.json'
        file_name = p + '/' + file_name
        maincheck_networkX(file_name, keys)

        print("G_10000_80000_1 :")
        file_name = 'data/G_10000_80000_1.json'
        file_name = p + '/' + file_name
        maincheck_networkX(file_name, keys)

        print("G_20000_160000_1 :")
        file_name = 'data/G_20000_160000_1.json'
        file_name = p + '/' + file_name
        maincheck_networkX(file_name, keys)

        print("G_30000_240000_1 :")
        file_name = 'data/G_30000_240000_1.json'
        file_name = p + '/' + file_name
        maincheck_networkX(file_name, keys)


if __name__ == '__main__':
    unittest.main()
