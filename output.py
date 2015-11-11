#!/usr/bin/env python

import networkx as nx
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def draw_graph(g, pos, round_no, messages, watched, draw_labels):
    # Draw this round's sharing
    # Draw what was seen and shared this round on the nodes
    #

    cmap = plt.get_cmap("Blues_r")
    # Under: shared
    cmap.set_under('orange')
    # Over: seen but not shared
    cmap.set_over('red')

    seen_colours = []
    for node_index in g.nodes_iter():
        # Only draw watched message as specific colour
        if (messages[watched] in g.node[node_index]['shared'][round_no]):
            seen_colours.append(-1)
        elif (messages[watched] in g.node[node_index]['seen'][round_no]):
            seen_colours.append(len(messages) + 1)
        else:
            # Gradient based on no of messages seen
            seen_colours.append(len(g.node[node_index]['seen'][round_no]))

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
    nodes = nx.draw_networkx_nodes(g, pos, node_size=150, font_color='orange',
                                   labels=labels, with_labels=draw_labels,
                                   node_color=seen_colours, vmin=0,
                                   vmax=len(messages), cmap=cmap,)

    nx.draw_networkx_edges(g, pos, width=2.0,
                           edge_color=shared_colours)

    cbar = plt.colorbar(nodes)
    cbar.ax.tick_params(axis='x', colors='white')
    cbar.ax.tick_params(axis='y', colors='white')

    plt.axis('off')

    plt.savefig("output/round{0}.png".format(round_no), dpi=80,
                facecolor='black')
    plt.close(fig)
