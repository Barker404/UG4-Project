import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edges_from([
    (1, 2), (1, 4), (2, 3), (2, 5), (3, 6),
    (4, 5), (4, 7), (5, 6), (5, 8), (6, 9),
    (7, 8), (8, 9)])
fig = plt.figure(figsize=(8, 8))
pos = dict(zip(
    G,
    [(0, 2), (1, 2), (2, 2),
     (0, 1), (1, 1), (2, 1),
     (0, 0), (1, 0), (2, 0)]))

print G.edges()

nodelist = [1, 2, 3, 4, 5, 6, 7, 8, 9]

ec = ['black', 'black', 'black', 'black', 'black',
      'black', 'black', 'black', 'black', 'black',
      'black', 'black']

nc = ['blue', 'blue', 'blue',
      'blue', 'blue', 'red',
      'blue', 'blue', 'blue']

nodes = nx.draw_networkx_nodes(G, pos, node_color=nc)
edges = nx.draw_networkx_edges(G, pos, edge_color=ec, width=4)

plt.axis('off')
plt.savefig("output/presOut6.png", dpi=80, facecolor='white')
