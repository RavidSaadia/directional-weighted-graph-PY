import copy
from heapq import heappush, heappop
from typing import List
from pathlib import Path

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
        return self._g

    def DFS_visit(self, u, time, pi, discovery, finishing):
        """
        ===dfs-visit(u)===
        1. color[u] ← GRAY (1)
        2. time ← time + 1
        3. d[u] ← time
        4. for each v ∈ Adj[u]
        5.  do if color[v] = WHITE
        6.      then π[v] ← u
        7.      DFS-Visit(v)
        8. color[u] ← BLACK (2)
        9. f[u] ← time ← time + 1
        """
        u.tag = 1
        time += 1
        discovery[u.id()] = time
        for v in self._g.all_out_edges_of_node(u.id()):
            v = self._g.get_all_v()[v]
            if v.tag == 0:
                pi[v.id()] = u.id()
                time = self.DFS_visit(v, time, pi, discovery, finishing)

        u.tag = 2
        time += 1
        finishing[u.id()] = time
        return time

    def dfs(self, nodes):
        """
        1. for each vertex u ∈ V[G]
        2.  do color[u] ← white (0)
        3.  π[u] ← NULL (-1)
        4. time ← 0
        5. for each vertex u ∈ V[G]
        6.  do if color[u] = white
        7.      then DFS-Visit(u)
        """
        discovery = {}
        finishing = {}
        pi = {}
        time = 0
        for u in nodes:
            u = self._g.get_all_v()[u]
            u.tag = 0
            pi[u.id()] = -1
        for u in nodes:
            u = self._g.get_all_v()[u]
            if u.tag == 0:
                time = self.DFS_visit(u, time, pi, discovery, finishing)
        return pi, discovery, finishing

    def transpose(self):
        g0 = DiGraph()
        for u in self._g.get_all_v().values():
            g0.add_node(u.id(), pos=copy.deepcopy(u.pos))
            for v, w in self._g.all_out_edges_of_node(u.id()).items():
                v = self._g.get_all_v()[v]
                g0.add_node(v.id(), pos=copy.deepcopy(v.pos))
                g0.add_edge(v.id(), u.id(), w)
        return g0

    def load_from_json(self, file_name: str) -> dict:
        p = str(Path(__file__).parent.parent)
        file_name = p + '/' + file_name
        with open(file_name, 'r') as fp:
            d = json.load(fp)
        self._g = DiGraph()
        for node in d['Nodes']:
            self._g.add_node(int(node['id']), tuple(map(float, node['pos'].split(','))))

        for edge in d['Edges']:
            self._g.add_edge(int(edge['src']), int(edge['dest']), float(edge['w']))

    def save_to_json(self, file_name: str) -> bool:
        d = {'Edges': [], 'Nodes': []}
        for key, node in self._g.get_all_v().items():
            d['Nodes'].append({'pos': str(node.pos)[1:-1].replace(' ', ''), 'id': key})

        for src in self._g.get_all_v().keys():
            for dest, w in self._g.all_out_edges_of_node(src).items():
                d['Edges'].append({'src': src, 'w': w, 'dest': dest})

        p = str(Path(__file__).parent.parent)
        file_name = p + '/' + file_name

        with open(file_name, 'w') as to_save:
            json.dump(d, to_save)

    def shortest_path(self, id1: int, id2: int) -> (float, list):

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
        return dist[id2], paths[id2]

    def connected_component(self, id1: int) -> list:
        c = self.connected_components()
        for res in c:
            if id1 in res:
                return res
        print(f"{id1} not in the graph")
        return []

    def connected_components(self) -> List[list]:
        """
        1. call DFS(G) to compute finishing times f [u] for all u
        2. compute GT
        3. call DFS(GT), but in the main loop, consider vertices in
        order of decreasing f [u] (as computed in first DFS)
        4. output the vertices in each tree of the depth-first forest
        formed in second DFS as a separate SCC
        """
        temp = self._g
        pi, discovery, finishing = self.dfs(self._g.get_all_v().keys())

        g0 = self.transpose()
        self.init(g0)
        pi2, discovery2, finishing2 = self.dfs(dict(sorted(finishing.items(), key=lambda item: item[1], reverse=True)).keys())
        res = []
        keys = list(finishing2.keys())
        while keys:
            k = keys.pop(0)
            con = [k]
            while pi2[k] != -1 and keys:
                k = pi2[k]
                if k in finishing2:
                    keys.pop(0)
                con.append(k)
            res.append(con)

        self.init(temp)
        return res

    def plot_graph(self) -> None:
        paint(self._g, title=str(self._g))


if __name__ == '__main__':
    pass
