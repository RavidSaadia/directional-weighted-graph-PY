import sys

import matplotlib.pyplot as plt
import numpy as np


def set_radius(g):
    maxx_pos = 0
    minx_pos = sys.float_info.max

    pos_zero = (0, 0, 0)
    for node in g.get_all_v().values():

        if dist(node.pos, pos_zero) > maxx_pos:
            maxx_pos = dist(node.pos, pos_zero)
        if dist(node.pos, pos_zero) < minx_pos:
            minx_pos = dist(node.pos, pos_zero)

    return (maxx_pos - minx_pos) * 0.0214


def dist(pos1, pos2):
    return np.sqrt(np.power(pos1[0] - pos2[0], 2) + np.power(pos1[1] - pos2[1], 2))


def get_point(s, e, r):

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


def paint(g, title="", show_w=False, t=False):
    r = set_radius(g)
    ax = plt.axes()
    edges_of_node = g.all_out_edges_of_node
    if t:
        edges_of_node = g.all_in_edges_of_node
    for Snode in g.get_all_v().values():
        Spos = Snode.pos
        ax.add_artist(plt.Circle(Spos, radius=r))
        Sid = Snode.id()
        ax.text(Spos[0], Spos[1], Sid,
                color=(1, 1, 1),
                ha='center',
                va='center')
        for key in edges_of_node(Sid):
            Enode = g.get_all_v()[key]
            Epos = Enode.pos
            pos = get_point(Spos, Epos, r)
            ax.arrow(Spos[0], Spos[1], pos[0] - Spos[0], pos[1] - Spos[1],
                     width=0.00001,
                     head_width=(0.015 * dist(Spos, pos) * r),
                     head_length=(0.03 * dist(Spos, pos) * r),
                     length_includes_head=True,
                     fc=(0.8, 0.2, 0.3, 1),
                     ec=(0.8, 0.2, 0.3, 1))
            if show_w:
                plt.text((Spos[0] + Epos[0]) / 2, (Spos[1] + Epos[1]) / 2, str(round(g.get_edge(Sid, key)[0], 2)),
                         ha='center',
                         va='center')
    plt.title(title)
    plt.title(f' r = {r}')
    plt.show()
