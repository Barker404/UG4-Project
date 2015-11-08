#!/usr/bin/env python

import networkx as nx
from random import uniform
from math import floor


def kleinberg(cols, rows, k, q):
    # k: no of random edges to generate
    # q: clustering exponent
    # Creates a grid of size rows * cols
    # For each node in the grid, add k random edges
    # Where the probability of a random edge from u to v is proportional to:
    # d(u, v)^q
    # Where d(u, v) is grid distance

    # Start with grid
    g = nx.grid_2d_graph(cols, rows)

    # Add k extra edges for each node
    for node_index in g.nodes_iter():
        for i in range(k):
            v_index = kleinberg_random_node(g, node_index, q)
            g.add_edge(node_index, v_index)
    return g


def kleinberg2(cols, rows, k, q):
    # k: no of random edges to generate
    # q: clustering exponent
    # Creates a grid of size rows * cols
    # For each node in the grid, add k random edges
    # Where the probability of a random edge from u to v is proportional to:
    # d(u, v)^q
    # Where d(u, v) is grid distance

    # Start with grid
    g = nx.grid_2d_graph(cols, rows)

    # Choose the center node as the one which will have the highest
    # probability sum (normalisation constant)
    norm_node = (floor(cols/2), floor(rows/2))

    # Take this normalisation constant and use it for all calculations
    # Less calculations to perform, however nodes closer to the outside are
    # more likely to have no long link (only the center node is gauranteed to
    # have one)
    constant = get_norm_const(g, norm_node, 2)

    # Add k extra edges for each node
    for node_index in g.nodes_iter():
        for i in range(k):
            v_index = kleinberg_random_node2(g, node_index, q, constant)
            if v_index is not None:
                g.add_edge(node_index, v_index)
    return g


def kleinberg_random_node(g, node_index, q):
    # Probability of choosing v given u is proportional to:
    # d(u, v)^q
    # Where d(u, v) is grid distance

    # Calculate sum of probabilities to get actual probabilities
    prob_sum = get_norm_const(g, node_index, q)

    # Take random number in [0, prob_sum]
    rand = uniform(0, prob_sum)
    for v_index in g.nodes_iter():
        # Skip the original node to avoid dividing by 0
        if v_index == node_index:
            continue

        # subtract d(u, v)^q from the random number
        # when it reaches 0, the current node is our randomly picked node
        d = grid_distance(node_index, v_index)
        rand -= pow(d, -q)
        if (rand <= 0):
            return v_index


def kleinberg_random_node2(g, node_index, q, prob_sum):
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
        d = grid_distance(node_index, v_index)
        rand -= pow(d, -q)
        if (rand <= 0):
            return v_index
    return None


def get_norm_const(g, node_index, q):
    # normalisation constant = sum(d(u, v)^q) over all v != u
    norm_const = 0
    for v_index in g.nodes_iter():
        # Skip the original node to avoid dividing by 0
        if v_index == node_index:
            continue

        d = grid_distance(node_index, v_index)
        norm_const += pow(d, -q)
    return norm_const


def grid_distance(u, v):
    # u, v must be 2-tuples of x, y coords in grid
    # Just take manhatten distance
    return abs(u[0] - v[0]) + abs(u[1] - v[1])
