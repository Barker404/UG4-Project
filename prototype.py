#!/usr/bin/env python

import networkx as nx
from collections import Counter
from random import random
import matplotlib.pyplot as plt


def ShowAlg(possible):
    counts = Counter(possible)
    top = counts.most_common(3)

    return [t[0] for t in top]


def ShareAlg(shown):
    SHARE_PROB = 0.3
    return [x for x in shown if random() > SHARE_PROB]


def drawGraph(g, pos, roundNo):
    # Draw this round's sharing
    seenColours = [len(g.node[nodeIndex]['seen'][roundNo]) for
                   nodeIndex in g.nodes_iter()]

    sharedColours = [int(
        (len(g.node[edge[0]]['shared'][roundNo]) > 0 or
         len(g.node[edge[1]]['shared'][roundNo]) > 0))
        for edge in g.edges()]

    nx.draw(g, pos, node_color=seenColours, edge_color=sharedColours,
            width=2.0, vmin=0.0, vmax=1.0, with_labels=False)
    plt.savefig("output/round{0}.png".format(roundNo), dpi=200,
                facecolor='black')
    plt.clf()


print "start"

ROWS = 10
COLUMNS = 10
ROUND_COUNT = 10
MESSAGE_COUNT = 1

# Create graph
g = nx.grid_2d_graph(COLUMNS, ROWS)
# Use node labels as positions
pos = dict(zip(g, g))
print "made graph"

# Set up node attributes
for i in g.nodes_iter():
    g.node[i]['seen'] = [[]]
    g.node[i]['shared'] = [[]]

# Set message starting points
# (uses the first k nodes)
iterator = g.nodes_iter()
for i in range(0, MESSAGE_COUNT):
    nodeIndex = iterator.next()

    # Assume starting node always shares
    g.node[nodeIndex]['seen'][0].append(i)
    g.node[nodeIndex]['shared'][0].append(i)

# Draw initial config
drawGraph(g, pos, 0)

# Simulate rounds
for roundNo in range(1, ROUND_COUNT + 1):
    print "ROUND {0}".format(roundNo)
    for nodeIndex in g.nodes_iter():

        # Get messages that could possiblu be shown
        possible = [g.node[n]['shared'][roundNo-1] for
                    n in g.neighbors_iter(nodeIndex)]
        # Flatten possible
        possible = [item for sublist in possible for item in sublist]

        # Update messages
        seen = ShowAlg(possible)
        g.node[nodeIndex]['seen'].append(seen)
        shared = ShareAlg(seen)
        g.node[nodeIndex]['shared'].append(shared)

    drawGraph(g, pos, roundNo)
