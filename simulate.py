#!/usr/bin/env python

from showing import show_alg
from sharing import share_alg
from output import draw_graph
from graph import kleinberg
from random import choice
from message import Message


print "start"

ROWS = 10
COLUMNS = 10
ROUND_COUNT = 20
MESSAGE_COUNT = 10

DRAW = True
WATCHED_MESSAGE = 0
DRAW_LABELS = False


def create_graph():
    # Create graph
    g = kleinberg(20, 20, 1, 2)
    pos = dict(zip(g, map((lambda (x, y): (x * 2, y * 2)), g)))
    print "made graph"

    # Set up node attributes
    for i in g.nodes_iter():
        g.node[i]['seen'] = [[]]
        g.node[i]['shared'] = [[]]

    return (g, pos)


def create_messages(g):

    messages = []

    for i in range(0, MESSAGE_COUNT):
        source_index = choice(g.nodes())
        destination_index = choice(g.nodes())
        message = Message(i, source_index, destination_index)
        messages.append(message)

        # Assume starting node always shares
        g.node[source_index]['seen'][0].append(message)
        g.node[source_index]['shared'][0].append(message)

    return (messages)


g, pos = create_graph()
messages = create_messages(g)

if DRAW:
    # Draw initial config
    draw_graph(g, pos, 0, messages, WATCHED_MESSAGE, DRAW_LABELS)

# Simulate rounds
for round_no in range(1, ROUND_COUNT + 1):
    print "ROUND {0}".format(round_no)
    for node_index in g.nodes_iter():

        # Get messages that could possibly be shown
        # possible has format [(message, previous_node)]
        # seen and shared are simply format [message]
        possible = [(message, neighbour)
                    for neighbour in g.neighbors_iter(node_index)
                    for message in g.node[neighbour]['shared'][round_no - 1]]

        # Update messages
        seen = show_alg(possible)

        g.node[node_index]['seen'].append(seen)
        for message in seen:
            if message.destination == node_index and not message.delivered:
                message.delivered = True
                print str(message.id) + " delivered!"

        shared = share_alg(seen)
        g.node[node_index]['shared'].append(shared)

    if DRAW:
        draw_graph(g, pos, round_no, messages, WATCHED_MESSAGE, DRAW_LABELS)


print "{0} out of {1} message were delivered".format(
    len([x for x in messages if x.delivered]), len(messages))
