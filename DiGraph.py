from GraphInterface import GraphInterface

from Node import *


class DiGraph(GraphInterface):

    def __init__(self, nodes: dict = {}):
        self._nodes = nodes
        self._e_size = 0
        self._mc = 0

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self._nodes.keys():
            return False
        self._e_size -= len(self._nodes[node_id].get_inside())
        self._e_size -= len(self._nodes[node_id].get_outside())
        self._mc += 1
        for n in list(self._nodes[node_id].get_outside().keys()):
            self.remove_edge(node_id, self._nodes[n].get_id())

        for n in list(self._nodes[node_id].get_inside().keys()):
            self.remove_edge(self._nodes[n].get_id(), node_id)
        del(self._nodes[node_id])
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self._nodes or node_id2 not in self._nodes:
            return False
        if node_id1 in self._nodes[node_id2].get_inside().keys():
            return False
        del(self._nodes[node_id1].get_outside()[node_id2])
        del(self._nodes[node_id2].get_inside()[node_id1])
        self._e_size -= 1
        self._mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self._nodes.keys():
            return False
        self._nodes[node_id] = Node({}, {}, '', 0, pos)
        self._mc += 1
        return True

    def v_size(self) -> int:
        return len(self._nodes)

    def e_size(self) -> int:
        return self._e_size

    def get_all_v(self) -> dict:
        return self._nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self._nodes[id1].get_inside()

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self._nodes[id1].get_outside()

    def get_mc(self) -> int:
        return self._mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self._nodes or id2 not in self._nodes:
            return False
        if id1 in self._nodes[id2].get_inside().keys():
            return False
        self._nodes[id1].get_outside()[id2] = weight
        self._nodes[id2].get_inside()[id1] = weight
        self._e_size += 1
        self._mc += 1
        return True

    def __repr__(self):
        return f'|V| = {self.v_size()} |E| = {self.e_size()}'


if __name__ == '__main__':
    g = DiGraph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_edge(0, 1, 8.3)
    g.add_edge(0, 2, 6.7)
    g.add_edge(2, 0, 5.3)
    g.add_edge(2, 1, 0.73)
    print(g.get_all_v()[2].get_inside())
    print(g.get_all_v()[2].get_outside())
    g.remove_node(0)
    print(g.get_all_v()[2].get_inside())
    print(g.get_all_v()[2].get_outside())
