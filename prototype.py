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

print "start"

NODE_COUNT = 30
ROUND_COUNT = 10
MESSAGE_COUNT = 1

# Create graph
g = nx.erdos_renyi_graph(NODE_COUNT, 0.2)
pos = nx.spring_layout(g)
print "made graph"

# Create message starting points
shared = []
for i in range(0, MESSAGE_COUNT):
    shared.append([[i]])
for i in range(MESSAGE_COUNT, NODE_COUNT):
    shared.append([[]])
print "setup messages"


# Simulate rounds
for roundNo in range(0, ROUND_COUNT):
    print "ROUND {0}".format(roundNo)
    for node in g.nodes_iter():

        # Get messages that could possiblu be shown
        possible = [shared[neighbour][roundNo] for 
            neighbour in g.neighbors_iter(node)]

        # Flatten possible
        possible = [item for sublist in possible for item in sublist]

        # Update messages
        shown = ShowAlg(possible)
        shared[node].append(ShareAlg(shown))

    # Draw this round's sharing
    colours = [len(shared[node][roundNo]) for node in g.nodes_iter()]
    nx.draw(g, pos, node_color=colours, vmin=0.0, vmax=1.0, with_labels=False)
    plt.savefig("round{0}.png".format(roundNo),dpi=75)
    plt.clf()

for roundShared in shared:
    print roundShared

raw_input("Press Enter to continue...\n")
