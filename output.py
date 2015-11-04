#!/usr/bin/env python

import networkx as nx
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def drawGraph(g, pos, roundNo, watched):
    # Draw this round's sharing
    seenColours = []
    for nodeIndex in g.nodes_iter():
        if watched is None or any(
                msg in g.node[nodeIndex]['seen'][roundNo] for msg in watched):
            seenColours.append(1)
        else:
            seenColours.append(0)

    sharedColours = []
    for edge in g.edges():
        if watched is None or any(
                (msg in g.node[edge[0]]['shared'][roundNo]) or
                (msg in g.node[edge[1]]['shared'][roundNo])
                for msg in watched):
            sharedColours.append(1)
        else:
            sharedColours.append(0)

    labels = {}
    for nodeIndex in g.nodes_iter():
        sharedSet = set(g.node[nodeIndex]['shared'][roundNo])
        seenSet = set(g.node[nodeIndex]['seen'][roundNo]) - sharedSet

        label = " ".join(map(str, sharedSet))
        if seenSet:
            label += "("
            label += ") (".join(map(str, seenSet))
            label += ")"

        labels[nodeIndex] = label

    nx.draw(g, pos, node_color=seenColours, edge_color=sharedColours,
            width=2.0, vmin=0.0, vmax=1.0, with_labels=True,
            labels=labels, font_color='white')

    plt.savefig("output/round{0}.png".format(roundNo), dpi=200,
                facecolor='black')
    plt.clf()
