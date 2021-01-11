import copy

from src.GraphInterface import GraphInterface
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
            """
            return dict with keys of node u
            such that (u,self) edge exists,
            with value of the edge's weight
            :return: dict
            """
            return self._inside

        def get_outside(self) -> dict:
            """
            return dict with keys of node u
            such that (self,u) edge exists,
            with value of the edge's weight
            :return: dict
            """
            return self._outside

        def id(self) -> int:
            """

            :return: the node's id
            """
            return self._id

        def set_in(self, key, w):
            """
            add in edge with key = key and weight = w
            :param key:
            :param w:
            """
            self._inside[key] = w

        def set_out(self, key, w):
            """
            add out edge with key = key and weight = w
            :param key:
            :param w:
            """
            self._outside[key] = w

        def del_in(self, key):
            """
            remove in edge
            :param key:
            :return:
            """
            self._inside.pop(key)

        def del_out(self, key):
            """
            remove out edge
            :param key:
            :return:
            """
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
        """
        remove node with key = node_id from the graph
        :param node_id:
        :return: True if node_id has been removed, False else
        """
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
        """
        remove the edge (node_id1,node_id2) from the graph.
        :param node_id1:
        :param node_id2:
        :return: True if the edge removed,
        False if nothing has been changed
        (for example if one of the keys doesn't exists
        or the edge itself doesn't exists.
        """
        if node_id1 not in self._nodes or node_id2 not in self._nodes:
            return False
        if node_id1 not in self._nodes[node_id2].get_inside().keys():
            return False
        self._nodes[node_id2].del_in(node_id1)
        self._e_size -= 1
        self._mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        add node with key = node_id.
        optional: set position with 2-tuple(x,y) coordinates.
        :param node_id:
        :param pos:
        :return: True if the node has been removed, False if nothing has changes.
        (for example if the node doesn't exists in the graph.
        """
        if node_id in self._nodes.keys():
            return False
        self._nodes[node_id] = DiGraph.Node(node_id, pos)
        self._mc += 1
        return True

    def v_size(self) -> int:
        """
        :return: number of nodes in the graph.
        """
        return len(self._nodes)

    def e_size(self) -> int:
        """
        :return: number of edges in the graph.
        """
        return self._e_size

    def get_all_v(self) -> dict:
        """
        :return: dictionary with keys represents all the nodes keys, the values are the nodes.
        """
        return self._nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        :param id1:
        :return: dictionary of the ingoing edges from key=id1
        """
        return self._nodes[id1].get_inside()

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        :param id1:
        :return: dictionary of the outgoing edges from key=id1
        """
        return self._nodes[id1].get_outside()

    def get_mc(self) -> int:
        """
        :return: number of changes made in the graph
        """
        return self._mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        add edge (id1,id2) with weight = weight to the graph.
        :param id1:
        :param id2:
        :param weight:
        :return: True iff the edge (id1,id2) wasn't existed before
        """
        if id1 == id2 or id1 not in self._nodes or id2 not in self._nodes:
            return False
        if id1 in self._nodes[id2].get_inside():
            return False
        self._nodes[id1].set_out(id2, weight)
        self._nodes[id2].set_in(id1, weight)
        self._e_size += 1
        self._mc += 1
        return True

    def get_edge(self, id1, id2) -> (float,bool):
        """
        :param id1:
        :param id2:
        :return: 2-tuple. 1st is the weight of edge (id1,id2) (-1 if not existed), 2nd is wether the edge was existed
        """
        if id1 == id2 or id1 not in self._nodes or id2 not in self._nodes or id2 not in self.all_out_edges_of_node(id1):
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

