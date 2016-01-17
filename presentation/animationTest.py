import numpy as np
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (2, 0)])
fig = plt.figure(figsize=(8, 8))
pos = dict(zip(G, zip(G, G)))
print pos
nc = np.random.random(3)
nodes = nx.draw_networkx_nodes(G, pos, node_color=nc)
edges = nx.draw_networkx_edges(G, pos)


def update(n):
    nc = np.random.random(3)
    ec = np.random.random(3)
    nodes = nx.draw_networkx_nodes(G, pos, node_color=nc)
    edges = nx.draw_networkx_edges(G, pos, edge_color=ec)
    return edges, nodes

anim = FuncAnimation(fig, update, interval=50, blit=True)

plt.show()