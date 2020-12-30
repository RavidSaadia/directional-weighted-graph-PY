from typing import List
from pathlib import Path
import GraphInterface
import json
from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g=None):
        self._g = g

    def init(self, graph):
        self._g = graph

    def get_graph(self) -> GraphInterface:
        return self._g

    #     {'Edges': [{'src': 0, 'w': 1.3118716362419698, 'dest': 16}, {'src': 0, 'w': 1.232037506070033, 'dest': 1},
    #                {'src': 1, 'w': 1.8635670623870366, 'dest': 0}, {'src': 1, 'w': 1.8015954015822042, 'dest': 2},
    #                {'src': 2, 'w': 1.5784991011275615, 'dest': 1}, {'src': 2, 'w': 1.0631605142699874, 'dest': 3},
    #                {'src': 2, 'w': 1.7938753352369698, 'dest': 6}, {'src': 3, 'w': 1.440561778177153, 'dest': 2},
    #                 ],
    #      'Nodes': [{'pos': '35.19589389346247,32.10152879327731,0.0', 'id': 0},
    #                {'pos': '35.20319591121872,32.10318254621849,0.0', 'id': 1},
    #                {'pos': '35.20752617756255,32.1025646605042,0.0', 'id': 2},
    #                {'pos': '35.21007339305892,32.10107446554622,0.0', 'id': 3},
    # ]}

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
        d = {}
        d['Edges'] = []
        d['Nodes'] = []
        print(self._g.get_all_v())
        for key, node in self._g.get_all_v().items():
            d['Nodes'].append({'pos': str(node.pos)[1:-1].replace(' ', ''), 'id': key})

        for src in self._g.get_all_v().keys():
            for dest, w in self._g.all_out_edges_of_node(src).items():
                d['Edges'].append({'src': src, 'w' : w, 'dest' : dest})

        p = str(Path(__file__).parent.parent)
        file_name = p + '/' + file_name

        with open(file_name, 'w') as to_save:
            json.dump(d, to_save)


    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass


if __name__ == '__main__':
    ga = GraphAlgo()
    ga.load_from_json('data/A1')
    print(ga.get_graph().get_all_v())
