import copy
from heapq import heappush, heappop
from typing import List
from random import Random as rnd
from src.Graphics import paint
import src.GraphInterface as GraphInterface
import json
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g=None):
        self._g = g

    def init(self, graph):
        self._g = graph

    def get_graph(self) -> GraphInterface:
        """
        :return: the initialized graph
        """
        return self._g

    def _DFS_visit(self, root, finishing, t):
        """
        private method in use by dfs().
        the pseudo code for recursive function is:
        1. color[u] = GRAY
        2. time = time + 1
        3. d[u] = time
        4. for each v in Adj[u]
        5.  do if color[v] = WHITE
        6.      then pi[v] = u
        7.      DFS-Visit(v)
        8. color[u] = BLACK
        9. f[u] = time = time + 1
        the code below is the 'while-version' of the pseudo code above.
        """
        nodes = []  # stack
        component = []
        vs = self._g.get_all_v()

        edges_of_node = self._g.all_out_edges_of_node
        if t:
            edges_of_node = self._g.all_in_edges_of_node

        nodes.append(root)

        while len(nodes) > 0:
            u = nodes[-1] # peek

            # this is backtraced node, we can remove it from stack
            if u.tag == 1:
                u.tag = 2  # black
                finishing.append(u.id())
                nodes.pop()
                continue

            # visit
            u.tag = 1

            # for SCC's
            component.append(u.id())

            for v in edges_of_node(u.id()):
                v = vs[v]
                if v.tag == 0:
                    nodes.append(v)
        return component

    def dfs(self, nodes, t=False):
        """
        simple dfs concept, with a touch of calculating the scc's inside the algorithm to save runtime.
        the pseudo code taken from algo1 lecture.
        1. for each vertex u ∈ V[G]
        2.  do color[u] ← white (0)
        3.  π[u] ← NULL (-1)
        4. time ← 0
        5. for each vertex u ∈ V[G]
        6.  do if color[u] = white
        7.      then DFS-Visit(u)
        """
        res = []
        finishing = []
        all_v = self._g.get_all_v()
        for u in nodes:
            u = all_v[u]
            u.tag = 0
        nodes_lst = nodes
        if not t:
            nodes_lst = list(nodes.keys())
        for u in reversed(nodes_lst):
            u = all_v[u]
            if u.tag == 0:
                con = self._DFS_visit(u, finishing, t)
                res.append(con)

        return finishing, res

    def transpose(self):
        """
        this method was written originally for SCC's,
        but a shortcut made by swapping all_out_edges_of_node with all_in_edges_of_node when needed.
        so the function remained for general purposes.
        """
        g0 = DiGraph()
        for u in self._g.get_all_v().values():
            g0.add_node(u.id(), pos=copy.deepcopy(u.pos))
            for v, w in self._g.all_out_edges_of_node(u.id()).items():
                v = self._g.get_all_v()[v]
                g0.add_node(v.id(), pos=copy.deepcopy(v.pos))
                g0.add_edge(v.id(), u.id(), w)
        return g0

    def load_from_json(self, file_name: str) -> dict:
        """
        load  a graph from a json file.
        the graph loaded will replace the initialized graph.
        """

        with open(file_name, 'r') as fp:
            d = json.load(fp)
        self._g = DiGraph()
        for node in d['Nodes']:
            r = rnd()
            pos = (r.random(), r.random(), r.random())
            if 'pos' in node:
                pos = tuple(map(float, node['pos'].split(',')))
            self._g.add_node(int(node['id']), pos)

        for edge in d['Edges']:
            self._g.add_edge(int(edge['src']), int(edge['dest']), float(edge['w']))

    def save_to_json(self, file_name: str) -> bool:
        """
        save the initialized graph to a file.
        """
        d = {'Edges': [], 'Nodes': []}
        for key, node in self._g.get_all_v().items():
            d['Nodes'].append({'pos': str(node.pos)[1:-1].replace(' ', ''), 'id': key})

        for src in self._g.get_all_v().keys():
            for dest, w in self._g.all_out_edges_of_node(src).items():
                d['Edges'].append({'src': src, 'w': w, 'dest': dest})

        with open(file_name, 'w') as to_save:
            json.dump(d, to_save)

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        calculate the shortest path from id1 to id2 using dijaxtra algorithm.
        :return: the weight of the path and a list with the path keys.
        if the path doesn't exist, return 'inf',[].
        """
        nodes = self._g.get_all_v().keys()
        paths = {id1: [id1]}
        push = heappush
        pop = heappop
        dist = {}  # dictionary of final distances
        seen = {}
        # q is heapq with 2-tuples (distance, node)
        q = []
        if id1 not in nodes:
            return float('inf'), []
        seen[id1] = 0
        push(q, (0, id1))
        while q:
            (d, v) = pop(q)  # d is distance, v is the new current node
            if v in dist:
                continue  # already searched this node.
            dist[v] = d
            if v == id2:
                break
            for u, e in self._g.all_out_edges_of_node(v).items():
                vu_dist = dist[v] + e  # id1->...->v->u
                if u in dist:
                    if vu_dist < dist[u]:  # optional
                        raise ValueError("Contradictory paths found:", "negative weights?")
                elif u not in seen or vu_dist < seen[u]:
                    seen[u] = vu_dist
                    push(q, (vu_dist, u))
                    if v not in paths:
                        paths[v] = [v]
                    paths[u] = paths[v] + [u]
        if id2 in dist and id2 in paths:
            return dist[id2], paths[id2]
        return float('inf'), []

    def connected_component(self, id1: int) -> list:
        """
        return the component that contains id1
        represented by list of the component's keys.
        if the key isn't in the initialized graph, return [].
        """
        c = self.connected_components()
        for res in c:
            if id1 in res:
                return res
        print(f"{id1} not in the graph")
        return []

    def connected_components(self) -> List[list]:
        """
        1. call DFS(G) to compute finishing times f [u] for all u
        2. compute G transpose (actually just swapping all_in_edges_of_node with all_out_edges_of_node)
        3. call DFS(G transpose), but in the main loop, consider vertices in
           order of decreasing f [u] (as computed in first DFS)
        4. output the vertices in each tree of the depth-first forest
           formed in second DFS as a separate SCC
        """

        finishing, res = self.dfs(self._g.get_all_v())

        finishing2, res = self.dfs(finishing, t=True)

        return res

    def plot_graph(self) -> None:
        """
        painting the graph using matplotlib (in 'Graphics.py')
        """
        paint(self._g, title=str(self._g))


if __name__ == '__main__':
    pass
