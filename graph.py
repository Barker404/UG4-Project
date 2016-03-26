#!/usr/bin/env python

import networkx as nx
from random import uniform
from math import floor, sqrt
import numpy as np

from abc import ABCMeta, abstractmethod


class GraphGenerator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_graph(self, g, node_index, possible):
        pass

    @abstractmethod
    def generate_positions(self, g):
        pass

    @abstractmethod
    def get_width(self, g):
        pass

    @abstractmethod
    def get_height(self, g):
        pass


class FileGraphGenerator(GraphGenerator):

    def __init__(self, path):
        self.path = path
        self.g = nx.read_edgelist(self.path)

    def generate_graph(self):
        g_copy = self.g.copy()
        g_info = GraphInfo(g_copy)
        return g_copy, g_info

    def generate_positions(self, g):
        return nx.spring_layout(g)

    def get_width(self, g):
        return sqrt(g.number_of_nodes)

    def get_height(self, g):
        return sqrt(g.number_of_nodes)


class GridGenerator(GraphGenerator):

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows

    def generate_graph(self):
        # Creates a grid of size rows * cols
        # For each node in the grid, add k random edges
        # Where the probability of an edge from u to v is proportional to:
        # d(u, v)^q
        # Where d(u, v) is grid distance

        # Start with grid
        g = nx.grid_2d_graph(self.cols, self.rows)
        g_info = GridGraphInfo(g)
        return g, g_info

    def generate_positions(self, g):
        return dict(zip(g, g))

    def get_width(self, g):
        return self.cols

    def get_height(self, g):
        return self.rows


class KleinbergGenerator(GridGenerator):

    def __init__(self, cols, rows, k, q):
        # k: no of random edges to generate
        # q: clustering exponent
        GridGenerator.__init__(self, cols, rows)
        self.k = k
        self. q = q

    def generate_graph(self):
        # Creates a grid of size rows * cols
        # For each node in the grid, add k random edges
        # Where the probability of an edge from u to v is proportional to:
        # d(u, v)^q
        # Where d(u, v) is grid distance

        # Start with grid
        g = nx.grid_2d_graph(self.cols, self.rows)
        g_info = GridGraphInfo(g)

        # Add k extra edges for each node
        for node_index in g.nodes_iter():
            for i in range(self.k):
                v_index = self.kleinberg_random_node(g, g_info, node_index)
                g.add_edge(node_index, v_index)
        return g, g_info

    def kleinberg_random_node(self, g, g_info, node_index):
        # Probability of choosing v given u is proportional to:
        # d(u, v)^q
        # Where d(u, v) is grid distance

        # Calculate sum of probabilities to get actual probabilities
        prob_sum = self.get_norm_const(g, g_info, node_index)

        # Take random number in [0, prob_sum]
        rand = uniform(0, prob_sum)
        for v_index in g.nodes_iter():
            # Skip the original node to avoid dividing by 0
            if v_index == node_index:
                continue

            # subtract d(u, v)^q from the random number
            # when it reaches 0, the current node is our randomly picked node
            d = g_info.grid_distance(node_index, v_index)
            rand -= pow(d, -self.q)
            if (rand <= 0):
                return v_index

    def get_norm_const(self, g, g_info, node_index):
        # normalisation constant = sum(d(u, v)^q) over all v != u
        norm_const = 0
        for v_index in g.nodes_iter():
            # Skip the original node to avoid dividing by 0
            if v_index == node_index:
                continue

            d = g_info.grid_distance(node_index, v_index)
            norm_const += pow(d, -self.q)
        return norm_const


class KleinbergGeneratorSameNorm(KleinbergGenerator):

    def __init__(self, cols, rows, k, q):
        KleinbergGenerator.__init__(self, cols, rows, k, q)

    def generate_graph(self):
        # Creates a grid of size rows * cols
        # For each node in the grid, add k random edges
        # Where the probability of an edge from u to v is proportional to:
        # d(u, v)^q
        # Where d(u, v) is grid distance

        # Start with grid
        g = nx.grid_2d_graph(self.cols, self.rows)
        g_info = GridGraphInfo(g)

        # Choose the center node as the one which will have the highest
        # probability sum (normalisation constant)
        norm_node = (floor(self.cols / 2), floor(self.rows / 2))

        # Take this normalisation constant and use it for all calculations
        # Less calculations to perform, however nodes closer to the outside are
        # more likely to have no long link (only the center node is gauranteed
        # to have one)
        constant = self.get_norm_const(g, g_info, norm_node)

        # Add k extra edges for each node
        for node_index in g.nodes_iter():
            for i in range(self.k):
                v_index = self.kleinberg_random_node(g, g_info, node_index,
                                                     constant)
                if v_index is not None:
                    g.add_edge(node_index, v_index)
        return g, g_info

    def kleinberg_random_node(self, g, g_info, node_index, prob_sum):
        # Probability of choosing v given u is proportional to:
        # d(u, v)^q
        # Where d(u, v) is grid distance

        # Use the provided constant as out probability sum
        # Take random number in [0, prob_sum]
        rand = uniform(0, prob_sum)
        for v_index in g.nodes_iter():
            # Skip the original node to avoid dividing by 0
            if v_index == node_index:
                continue

            # subtract d(u, v)^q from the random number
            # when it reaches 0, the current node is our randomly picked node
            d = g_info.grid_distance(node_index, v_index)
            rand -= pow(d, -self.q)
            if (rand <= 0):
                return v_index
        return None


class GraphInfo(object):
    def __init__(self, g):
        self.g = g
        self._graph_distances = None
        self._diffusion_distances = {}
        self.diameter = None

    def get_diameter(self):
        if self.diameter is None:
            self.diameter = nx.diameter(self.g)
        return self.diameter

    def graph_distance(self, u, v):
        if self._graph_distances is None:
            self._graph_distances = nx.all_pairs_shortest_path_length(self.g)
        return self._graph_distances[u][v]

    def diffusion_distance(self, u, v, t):
        if t not in self._diffusion_distances:
            # Calculate Z: the (lazy) random walk transition probabilities
            a = nx.adjacency_matrix(self.g)
            d = np.matrix(np.diag(
                [self.g.degree(n) for n in self.g.nodes_iter()]))
            i = np.matrix(np.identity(self.g.number_of_nodes()))
            z = 0.5 * (i + d.I * a)
            # Z^t gives the probability of walking from one node to another in
            # t steps
            zt = z**t
            diff_mat = [
                [np.linalg.norm(zt[i] - zt[j])
                    for i in range(zt.shape[0])]
                for j in range(zt.shape[0])]

            self._diffusion_distances[t] = {}
            for i, ilabel in zip(range(self.g.number_of_nodes()),
                                 self.g.nodes_iter()):
                self._diffusion_distances[t][ilabel] = {}
                for j, jlabel in zip(range(self.g.number_of_nodes()),
                                     self.g.nodes_iter()):
                    self._diffusion_distances[t][ilabel][jlabel] = \
                        diff_mat[i][j]

        return self._diffusion_distances[t][u][v]


class GridGraphInfo(GraphInfo):
    def grid_distance(self, u, v):
        # u, v must be 2-tuples of x, y coords in grid
        # Just take manhatten distance
        return abs(u[0] - v[0]) + abs(u[1] - v[1])
