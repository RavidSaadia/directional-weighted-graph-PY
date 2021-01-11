import copy
import unittest

from src.DiGraph import DiGraph

key = -1


def get_new_key():
    global key
    key += 1
    return key


g = DiGraph()
a, b, c, d = [get_new_key() for _ in range(4)]
g.add_node(a)
g.add_node(b)
g.add_node(c)
g.add_node(d)
g.add_edge(a, b, 8.3)
g.add_edge(a, c, 6.7)
g.add_edge(c, a, 5.3)
g.add_edge(c, b, 0.73)
g.add_edge(d, b, 4.73)
g.add_edge(d, b, 4.73)


class MyTestCase(unittest.TestCase):
    def test_remove_node(self):
        g0 = copy.deepcopy(g)
        size = g0.v_size()
        g0.remove_node(0)
        self.assertEqual(g0.v_size(), size - 1)

    def test_add_node(self):
        g0 = copy.deepcopy(g)
        size = g0.v_size()
        g0.add_node(get_new_key())
        g0.add_node(get_new_key())
        self.assertEqual(g0.v_size(), size + 2)

    def test_remove_edge(self):
        g0 = copy.deepcopy(g)
        size = g0.e_size()
        g0.remove_edge(0, 1)
        self.assertEqual(g0.e_size(), size - 1)
        self.assertEqual(g0.e_size(), size - 1)

    def test_add_edge(self):
        g0 = copy.deepcopy(g)
        self.assertEqual(True, g0.add_edge(c, d, 9.9))
        self.assertEqual(True, g0.add_edge(b, d, 10))
        self.assertEqual(False, g0.add_edge(a, b, 10))  # exists

    def test_get_edge(self):
        g0 = copy.deepcopy(g)
        w = g0.get_edge(0, 1)[0]
        e = get_new_key()
        g0.add_node(e)
        g0.add_edge(0, e, w)
        self.assertEqual(g0.get_edge(0, 1), g0.get_edge(0, e))

    def test_mc(self):
        g0 = copy.deepcopy(g)
        g0.remove_edge(a, b)
        g0.remove_edge(a, b)
        self.assertEqual(g0.get_mc(), 10)

    def test_all_in_edge(self):
        g0 = copy.deepcopy(g)
        self.assertEqual(len(g0.all_in_edges_of_node(b)), 3)

    def test_all_out_edge(self):
        g0 = copy.deepcopy(g)
        self.assertEqual(len(g0.all_out_edges_of_node(b)), 0)


if __name__ == '__main__':
    unittest.main()
