import matplotlib.pyplot as plt
from src.GraphAlgo import GraphAlgo as ga
import numpy as np

r = 0.0003


def dist(pos1, pos2):
    return np.sqrt(np.power(pos1[0] - pos2[0], 2) + np.power(pos1[1] - pos2[1], 2))


def get_point(s, e):
    x1, y1 = s[0], s[1]
    x2, y2 = e[0], e[1]
    d = dist(s, e)
    dirX = (x1 - x2) / d
    dirY = (y1 - y2) / d
    x = dirX * r + x2
    y = dirY * r + y2

    return x, y


# def eden(s,e):
#     x1, y1 = s[0], s[1]
#     x2, y2 = e[0], e[1]
#     d = dist(s, e)-r
#     x = (x1*r+x2*d)/(r+d)
#     y = (y1*r+y2*d)/(r+d)
#     return x, y


def paint(g, seed):
    ax = plt.axes()
    for Snode in g.get_all_v().values():
        Spos = Snode.pos
        ax.add_artist(plt.Circle(Spos, radius=r))
        Sid = Snode.id()
        for key in g.all_out_edges_of_node(Sid):
            Enode = g.get_all_v()[key]
            Epos = Enode.pos
            pos = get_point(Spos, Epos)
            ax.arrow(Spos[0], Spos[1], pos[0] - Spos[0], pos[1] - Spos[1],
                     width=0.00001,
                     head_width=min(0.04 * dist(Spos, pos), 0.0003),
                     head_length=min(0.12 * dist(Spos, pos), 0.0008),
                     length_includes_head=True,
                     fc=(0.8, 0.2, 0.3, 1),
                     ec=(0.8, 0.2, 0.3, 1))
    plt.title(f'graph seed: {seed}')
    plt.show()
