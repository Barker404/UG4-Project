#!/usr/bin/env python

import os
import networkx as nx
import matplotlib
from matplotlib import animation
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt


SHARED_COLOUR = '#FF8000'
SEEN_COLOUR = '#FF0000'
DESTINATION_COLOUR = '#FF0080'

# Multiply the number of nodes along one axis by this to get the figure size
# along that axis
FIGSIZE_NODE_RATIO = 1.0 / 3.0
# Multiply the figure size width by this to make space for the colorbar
COLORBAR_FIGSIZE_RATIO = 4.0 / 3.0

NODE_SIZE = 50
DEST_NODE_SIZE = 100
EDGE_WIDTH = 2


class Visualiser(object):

    def __init__(self, columns, rows, output_path='output'):
        # Set the size of the figure based on the number of nodes in each
        # direction
        # Also take into account additional space for colourbar
        self.fig = plt.figure(figsize=(
            columns * COLORBAR_FIGSIZE_RATIO * FIGSIZE_NODE_RATIO,
            rows * FIGSIZE_NODE_RATIO))
        self.cbar_drawn = False
        self.output_path = output_path

        plt.axis('off')
        ax = plt.gca()
        ax.set_axis_bgcolor('black')

    def draw_image(self, g, pos, round_no, messages, max_seen, watched,
                   draw_labels):
        self._draw_frame(g, pos, round_no, messages, max_seen, watched,
                         draw_labels)
        try:
            os.makedirs(self.output_path)
        except OSError:
            if not os.path.isdir(self.output_path):
                raise

        plt.savefig(
            os.path.join(self.output_path, "round{0}.png".format(round_no)),
            dpi=150, facecolor='black')

    def create_video(self, g, pos, round_count, messages, max_seen, watched,
                     draw_labels):
        anim = animation.FuncAnimation(
            self.fig,
            lambda i: self._draw_frame(
                g, pos, i, messages,
                max_seen, watched,
                draw_labels),
            frames=round_count, interval=1000, blit=True)

        FFwriter = animation.FFMpegWriter(fps=1)
        try:
            os.makedirs(self.output_path)
        except OSError:
            if not os.path.isdir(self.output_path):
                raise
        anim.save(os.path.join(self.output_path, 'animation.mp4'),
                  writer=FFwriter, dpi=150, codec="libx264", bitrate=-1,
                  savefig_kwargs={'facecolor': 'black'})

    def _draw_frame(self, g, pos, round_no, messages, max_seen, watched,
                    draw_labels):
        # Draw this round's sharing
        # Draw what was seen and shared this round on the nodes
        self.fig.clear()

        cmap = plt.get_cmap("Blues_r")
        cmap_nodelist = []
        cmap_colours = []

        watched_nodelist = []
        watched_colours = []

        dest_nodelist = []
        dest_colours = []

        for node_index in g.nodes_iter():
            dest_node = False
            # Draw destination node up to and including delivery round
            if (messages[watched].destination == node_index and
                (not messages[watched].delivered or
                    messages[watched].delivery_turn == round_no)):
                dest_nodelist.append(node_index)
                dest_colours.append(DESTINATION_COLOUR)
                dest_node = True

            # Draw watched message as specific colour
            if (messages[watched] in g.node[node_index]['shared'][round_no]):
                watched_nodelist.append(node_index)
                watched_colours.append(SHARED_COLOUR)
            elif (messages[watched] in g.node[node_index]['seen'][round_no]):
                watched_nodelist.append(node_index)
                watched_colours.append(SEEN_COLOUR)
            elif not dest_node:
                # Don't draw normal cmap if destination node -
                # Should already have been added to that list
                # Gradient based on no of messages seen
                cmapValue = float(len(g.node[node_index]['seen'][round_no]))
                cmap_nodelist.append(node_index)
                cmap_colours.append(cmapValue)

        # Draw where the "seen" messages were shared from (last round) on the
        # edges
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
            labels = self.get_labels(g, round_no)

        # Draw the destination node, the nodes with the watched message, and
        # all other nodes seperately

        nodes_d = nx.draw_networkx_nodes(
            g, pos, nodelist=dest_nodelist, node_size=DEST_NODE_SIZE,
            node_shape='s', node_color=dest_colours,
            with_labels=draw_labels, labels=labels, font_color='orange')

        nodes_w = nx.draw_networkx_nodes(
            g, pos, nodelist=watched_nodelist, node_size=NODE_SIZE,
            node_shape='^', node_color=watched_colours,
            with_labels=draw_labels, labels=labels, font_color='orange')

        nodes_c = nx.draw_networkx_nodes(
            g, pos, nodelist=cmap_nodelist, node_size=NODE_SIZE,
            node_shape='o', node_color=cmap_colours,
            cmap=cmap, vmin=0, vmax=max_seen,
            with_labels=draw_labels, labels=labels, font_color='orange')

        edges = nx.draw_networkx_edges(g, pos, width=EDGE_WIDTH,
                                       edge_color=shared_colours)

        cbar = plt.colorbar(nodes_c)
        cbar.ax.tick_params(axis='x', colors='white')
        cbar.ax.tick_params(axis='y', colors='white')
        plt.axis('off')
        ax = plt.gca()
        ax.set_axis_bgcolor('black')

        return edges, nodes_w, nodes_d, nodes_c

    def get_labels(self, g, round_no):
        labels = {}
        for node_index in g.nodes_iter():
            shared_set = set(g.node[node_index]['shared'][round_no])
            seen_set = set(g.node[node_index]['seen'][round_no]) - \
                shared_set

            label = " ".join(map(lambda x: str(x.id), shared_set))
            if seen_set:
                label += " ("
                label += ") (".join(map(lambda x: str(x.id), seen_set))
                label += ")"

            labels[node_index] = label
        return labels


def plot_simulations(simulations, x_values, x_label, repeats,
                     output_path='output'):

    averages, mins, maxs = map(
        list, zip(*[
            sim.repeat_simulation(repeats, as_percent=True)
            for sim in simulations]))

    # Might want to do something with mins/maxes in future
    fig = plt.figure(figsize=(10, 10))
    plt.plot(x_values, averages, 'bo')

    x1, x2, y1, y2 = plt.axis()
    plt.axis((0, x2, 0, 100))
    plt.xlabel(x_label)
    plt.ylabel('Average % of messages delivered')

    try:
        os.makedirs(output_path)
    except OSError:
        if not os.path.isdir(output_path):
            raise
    plt.savefig(os.path.join(output_path, "plot.png"), dpi=150)
    print "plot saved"
