import copy

from GraphInterface import GraphInterface
from random import random as rnd


class DiGraph(GraphInterface):

    class Node:

        def __init__(self, i, pos: tuple = ()):
            self._inside: dict = {}
            self._outside: dict = {}
            self._id = i
            self.info: str = ""
            self.tag: float = 0
            self.pos = pos

        def get_inside(self) -> dict:
            return self._inside

        def get_outside(self) -> dict:
            return self._outside

        def id(self) -> int:
            return self._id

        def set_in(self, key, w):
            self._inside[key] = w

        def set_out(self, key, w):
            self._outside[key] = w

        def del_in(self, key):
            self._inside.pop(key)

        def del_out(self, key):
            self._outside.pop(key)

        def __eq__(self, other):
            return self._id == other.id()

        def __repr__(self):
            return str(self._outside)

    def __init__(self):
        self._nodes = {}
        self._e_size = 0
        self._mc = 0

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self._nodes:
            return False
        self._e_size -= len(self._nodes[node_id].get_inside())
        self._e_size -= len(self._nodes[node_id].get_outside())
        self._mc += 1

        for n in list(self._nodes[node_id].get_inside().keys()):
            self._nodes[n].del_in(node_id)

        self._nodes.pop(node_id)
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self._nodes or node_id2 not in self._nodes:
            return False
        if node_id1 not in self._nodes[node_id2].get_inside().keys():
            return False
        self._nodes[node_id2].del_in(node_id1)
        self._e_size -= 1
        self._mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self._nodes.keys():
            return False
        self._nodes[node_id] = DiGraph.Node(node_id, pos)
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
        if  id1 == id2 or id1 not in self._nodes or id2 not in self._nodes:
            return False
        if id1 in self._nodes[id2].get_inside():
            return False
        self._nodes[id1].set_out(id2, weight)
        self._nodes[id2].set_in(id1, weight)
        self._e_size += 1
        self._mc += 1
        return True

    def get_edge(self, id1, id2) -> float:
        if(id1 not in self._nodes or id2 not in self._nodes or id2 not in self.all_out_edges_of_node(id1)):
            return -1, False
        return self._nodes[id1].get_outside()[id2], True

    def __eq__(self, other):
        b = self._nodes == other.get_all_v()
        for src in self._nodes.keys():
            for dest in self.all_out_edges_of_node(src):
                b &= other.get_edge(src, dest)[1]
                b &= self.get_edge(src, dest) == other.get_edge(src, dest)
        return b

    def __repr__(self):
        return f'|V| = {self.v_size()} |E| = {self.e_size()}'

