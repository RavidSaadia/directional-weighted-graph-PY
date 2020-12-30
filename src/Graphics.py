import matplotlib.pyplot as plt
from GraphAlgo import GraphAlgo as ga
import numpy as np


def dist(pos1, pos2):
    return np.sqrt(np.power(pos1[0]-pos2[0],2)+np.power(pos1[1]-pos2[1],2))

gal = ga()
gal.load_from_json('data/A1')
g = gal.get_graph()
ax = plt.axes()
r = 0.0002
for snode in g.get_all_v().values():
    Spos = snode.pos
    ax.add_artist(plt.Circle(Spos,radius=r))
    Sid = snode.id()
    for key in g.all_out_edges_of_node(Sid):
        enode = g.get_all_v()[key]
        Epos = enode.pos
        ax.add_artist(plt.Circle(Epos,radius=r))

        ax.arrow(Spos[0], Spos[1], Epos[0]-Spos[0], Epos[1]-Spos[1],width=0.00001, head_width=0.04 * dist(Spos,Epos), head_length=0.12 * dist(Spos,Epos),length_includes_head=True, fc='k', ec='k')


plt.show()
plt.show()
