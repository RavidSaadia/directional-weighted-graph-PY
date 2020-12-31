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
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        paint(self._g, title=str(self._g))


if __name__ == '__main__':
    pass