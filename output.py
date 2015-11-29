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
TARGET_COLOUR = '#FF00FF'


def draw_graph(g, pos, round_no, messages, max_seen, watched, draw_labels):
    # Draw this round's sharing
    # Draw what was seen and shared this round on the nodes

    cmap = plt.get_cmap("Blues_r")
    # Under: shared
    cmap.set_under('orange')
    # Over: seen but not shared
    cmap.set_over('red')

    gradient_nodelist = []
    gradient_colours = []

    specific_nodelist = []
    specific_colours = []

    for node_index in g.nodes_iter():
        # Draw watched message as specific colour
        if (messages[watched] in g.node[node_index]['shared'][round_no]):
            specific_nodelist.append(node_index)
            specific_colours.append(SHARED_COLOUR)
        elif (messages[watched] in g.node[node_index]['seen'][round_no]):
            specific_nodelist.append(node_index)
            specific_colours.append(SEEN_COLOUR)
        elif (messages[watched].destination == node_index):
            specific_nodelist.append(node_index)
            specific_colours.append(TARGET_COLOUR)
        else:
            # Gradient based on no of messages seen
            cmapValue = float(len(g.node[node_index]['seen'][round_no]))
            gradient_nodelist.append(node_index)
            gradient_colours.append(cmapValue)

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

    fig = plt.figure(figsize=(20, 15))
    nx.draw_networkx_nodes(g, pos, nodelist=specific_nodelist, node_size=150,
                           font_color='orange', with_labels=draw_labels,
                           labels=labels, node_color=specific_colours)

    nodes = nx.draw_networkx_nodes(g, pos, nodelist=gradient_nodelist,
                                   node_size=150, font_color='orange',
                                   with_labels=draw_labels, labels=labels,
                                   node_color=gradient_colours, vmin=0,
                                   vmax=max_seen, cmap=cmap)

    nx.draw_networkx_edges(g, pos, width=2.0,
                           edge_color=shared_colours)

    cbar = plt.colorbar(nodes)
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
