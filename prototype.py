#!/usr/bin/env python

import networkx as nx

from showing import show_alg
from sharing import share_alg
from output import draw_graph

print "start"

ROWS = 10
COLUMNS = 10
ROUND_COUNT = 10
MESSAGE_COUNT = 1
MESSAGE_STARTS = None
WATCHED_MESSAGES = [0]


def create_graph():
    # Create graph
    g = nx.grid_2d_graph(COLUMNS, ROWS)
    # Use node labels as positions
    pos = dict(zip(g, g))
    print "made graph"

    # Set up node attributes
    for i in g.nodes_iter():
        g.node[i]['seen'] = [[]]
        g.node[i]['shared'] = [[]]

    return (g, pos)


def create_messages(g):
    # Set message starting points
    if MESSAGE_STARTS is None:
        iterator = g.nodes_iter()
    else:
        # If not given, just choose first n nodes
        iterator = iter(MESSAGE_STARTS)

    for i in range(0, MESSAGE_COUNT):
        node_index = iterator.next()

        # Assume starting node always shares
        g.node[node_index]['seen'][0].append(i)
        g.node[node_index]['shared'][0].append(i)


g, pos = create_graph()
create_messages(g)
# Draw initial config
draw_graph(g, pos, 0, WATCHED_MESSAGES)

# Simulate rounds
for round_no in range(1, ROUND_COUNT + 1):
    print "ROUND {0}".format(round_no)
    for node_index in g.nodes_iter():

        # Get messages that could possibly be shown
        possible = [g.node[n]['shared'][round_no - 1] for
                    n in g.neighbors_iter(node_index)]
        # Flatten possible
        possible = [item for sublist in possible for item in sublist]

        # Update messages
        seen = show_alg(possible)
        g.node[node_index]['seen'].append(seen)
        shared = share_alg(seen)
        g.node[node_index]['shared'].append(shared)

    draw_graph(g, pos, round_no, WATCHED_MESSAGES)
