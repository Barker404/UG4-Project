#!/usr/bin/env python

import os
import networkx as nx
import matplotlib
from matplotlib.colors import rgb2hex
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt


SHARED_COLOUR = '#FF8000'
SEEN_COLOUR = '#FF0000'
DESTINATION_COLOUR = '#FF0080'

# Multiply the number of nodes along one axis by this to get the figure size
# along that axis
FIGSIZE_NODE_RATIO = 1.0/3.0
# Multiply the figure size width by this to make space for the colorbar
COLORBAR_FIGSIZE_RATIO = 4.0/3.0

NODE_SIZE = 50
DEST_NODE_SIZE = 100
EDGE_WIDTH = 2


def draw_graph(g, pos, round_no, messages, max_seen, watched, draw_labels,
               width, height):
    # Draw this round's sharing
    # Draw what was seen and shared this round on the nodes

    cmap = plt.get_cmap("Blues_r")
    # Under: shared
    cmap.set_under('orange')
    # Over: seen but not shared
    cmap.set_over('red')

    cmap_nodelist = []
    cmap_colours = []

    watched_nodelist = []
    watched_colours = []

    dest_nodelist = []
    dest_colours = []

    for node_index in g.nodes_iter():
        # Draw watched message as specific colour
        if (messages[watched] in g.node[node_index]['shared'][round_no]):
            watched_nodelist.append(node_index)
            watched_colours.append(SHARED_COLOUR)
        elif (messages[watched] in g.node[node_index]['seen'][round_no]):
            watched_nodelist.append(node_index)
            watched_colours.append(SEEN_COLOUR)
        elif (messages[watched].destination == node_index):
            dest_nodelist.append(node_index)
            dest_colours.append(DESTINATION_COLOUR)
        else:
            # Gradient based on no of messages seen
            cmapValue = float(len(g.node[node_index]['seen'][round_no]))
            cmap_nodelist.append(node_index)
            cmap_colours.append(cmapValue)

    # Draw where the "seen" messages were shared from (last round) on the edges
    shared_colours = []
    for edge in g.edges():
        if ((messages[watched] in
                g.node[edge[0]]['shared'][round_no - 1]) or
            (messages[watched] in
                g.node[edge[1]]['shared'][round_no - 1])):
            shared_colours.append(1)
        else:
            shared_colours.append(0)

    labels = {}
    if (draw_labels):
        for node_index in g.nodes_iter():
            shared_set = set(g.node[node_index]['shared'][round_no])
            seen_set = set(g.node[node_index]['seen'][round_no]) - shared_set

            label = " ".join(map(lambda x: str(x.id), shared_set))
            if seen_set:
                label += " ("
                label += ") (".join(map(lambda x: str(x.id), seen_set))
                label += ")"

            labels[node_index] = label

    # Set the size of the figure based on the number of nodes in each direction
    # Also take into account additional space for colourbar
    fig = plt.figure(figsize=(width*COLORBAR_FIGSIZE_RATIO*FIGSIZE_NODE_RATIO,
                              height*FIGSIZE_NODE_RATIO))

    # Draw the nodes with the watched message, the destination node, and all
    # other nodes seperately
    nx.draw_networkx_nodes(g, pos, nodelist=watched_nodelist,
                           node_size=NODE_SIZE, node_color=watched_colours,
                           with_labels=draw_labels, labels=labels,
                           font_color='orange')

    nx.draw_networkx_nodes(g, pos, nodelist=dest_nodelist,
                           node_size=DEST_NODE_SIZE, node_color=dest_colours,
                           with_labels=draw_labels, labels=labels,
                           font_color='orange')

    n = nx.draw_networkx_nodes(g, pos, nodelist=cmap_nodelist,
                               node_size=NODE_SIZE, node_color=cmap_colours,
                               cmap=cmap, vmin=0, vmax=max_seen,
                               with_labels=draw_labels, labels=labels,
                               font_color='orange')

    nx.draw_networkx_edges(g, pos, width=EDGE_WIDTH,
                           edge_color=shared_colours)

    cbar = plt.colorbar(n)
    cbar.ax.tick_params(axis='x', colors='white')
    cbar.ax.tick_params(axis='y', colors='white')

    plt.axis('off')

    try:
        os.makedirs("output")
    except OSError:
        if not os.path.isdir("output"):
            raise

    plt.savefig("output/round{0}.png".format(round_no), dpi=80,
                facecolor='black')
    plt.close(fig)
