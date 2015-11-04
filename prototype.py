#!/usr/bin/env python

import networkx as nx

from showing import ShowAlg
from sharing import ShareAlg
from output import drawGraph

print "start"

ROWS = 10
COLUMNS = 10
ROUND_COUNT = 10
MESSAGE_COUNT = 1
MESSAGE_STARTS = None
WATCHED_MESSAGES = [0]

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
if MESSAGE_STARTS is None:
    iterator = g.nodes_iter()
else:
    iterator = iter(MESSAGE_STARTS)

for i in range(0, MESSAGE_COUNT):
    nodeIndex = iterator.next()

    # Assume starting node always shares
    g.node[nodeIndex]['seen'][0].append(i)
    g.node[nodeIndex]['shared'][0].append(i)

# Draw initial config
drawGraph(g, pos, 0, WATCHED_MESSAGES)

# Simulate rounds
for roundNo in range(1, ROUND_COUNT + 1):
    print "ROUND {0}".format(roundNo)
    for nodeIndex in g.nodes_iter():

        # Get messages that could possibly be shown
        possible = [g.node[n]['shared'][roundNo - 1] for
                    n in g.neighbors_iter(nodeIndex)]
        # Flatten possible
        possible = [item for sublist in possible for item in sublist]

        # Update messages
        seen = ShowAlg(possible)
        g.node[nodeIndex]['seen'].append(seen)
        shared = ShareAlg(seen)
        g.node[nodeIndex]['shared'].append(shared)

    drawGraph(g, pos, roundNo, WATCHED_MESSAGES)
