#!/usr/bin/env python

import networkx as nx
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def draw_graph(g, pos, round_no, watched):
    # Draw this round's sharing
    seen_colours = []
    for node_index in g.nodes_iter():
        if watched is None or any(
                msg in g.node[node_index]['seen'][round_no]
                for msg in watched):
            seen_colours.append(1)
        else:
            seen_colours.append(0)

    shared_colours = []
    for edge in g.edges():
        if watched is None or any(
                (msg in g.node[edge[0]]['shared'][round_no]) or
                (msg in g.node[edge[1]]['shared'][round_no])
                for msg in watched):
            shared_colours.append(1)
        else:
            shared_colours.append(0)

    labels = {}
    for node_index in g.nodes_iter():
        shared_set = set(g.node[node_index]['shared'][round_no])
        seen_set = set(g.node[node_index]['seen'][round_no]) - shared_set

        label = " ".join(map(str, shared_set))
        if seen_set:
            label += "("
            label += ") (".join(map(str, seen_set))
            label += ")"

        labels[node_index] = label

    nx.draw(g, pos, node_color=seen_colours, edge_color=shared_colours,
            width=2.0, vmin=0.0, vmax=1.0, with_labels=True,
            labels=labels, font_color='white')

    plt.savefig("output/round{0}.png".format(round_no), dpi=200,
                facecolor='black')
    plt.clf()
