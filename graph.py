#!/usr/bin/env python

import networkx as nx
from random import random, uniform
from math import floor


def kleinberg(cols, rows, k, q):
    # k: no of random edges to generate
    # q: clustering exponent
    # Creates a grid of size rows * cols
    # For each node in the grid, add k random edges
    # Where the probability of a random edge from u to v is proportional to:
    # d(u, v)^q
    # Where d(u, v) is grid distance

    g = nx.grid_2d_graph(cols, rows)
    for node_index in g.nodes_iter():
        for i in range(k):
            v_index = choose_random_node(g, node_index, q)
            g.add_edge(node_index, v_index)
    return g


def kleinberg2(cols, rows, k, q):
    g = nx.grid_2d_graph(cols, rows)
    for node_index in g.nodes_iter():
        for i in range(k):
            v_index = choose_random_node2(g, node_index, q)
            g.add_edge(node_index, v_index)
    return g


def kleinberg3(cols, rows, k, q):
    g = nx.grid_2d_graph(cols, rows)

    norm_node = (floor(cols/2), floor(rows/2))

    constant = get_norm_const(g, norm_node, 2)

    for node_index in g.nodes_iter():
        for i in range(k):
            v_index = choose_random_node3(g, node_index, q, constant)
            if v_index is not None:
                g.add_edge(node_index, v_index)
    return g


def choose_random_node(g, node_index, q):
    # calculate normalisation constant to get actual probabilities
    norm_const = get_norm_const(g, node_index, q)
    inv_norm_const = 1.0/norm_const

    rand = random()
    for v_index in g.nodes_iter():
        if v_index == node_index:
            continue

        d = grid_distance(node_index, v_index)
        rand -= inv_norm_const * pow(d, -q)
        if (rand < 0):
            return v_index


def choose_random_node2(g, node_index, q):
    # calculate normalisation constant to get actual probabilities
    norm_const = get_norm_const(g, node_index, q)

    rand = uniform(0, norm_const)
    for v_index in g.nodes_iter():
        if v_index == node_index:
            continue

        d = grid_distance(node_index, v_index)
        rand -= pow(d, -q)
        if (rand <= 0):
            return v_index


def choose_random_node3(g, node_index, q, norm_const):
    rand = uniform(0, norm_const)
    for v_index in g.nodes_iter():
        if v_index == node_index:
            continue

        d = grid_distance(node_index, v_index)
        rand -= pow(d, -q)
        if (rand <= 0):
            return v_index
    return None


def get_norm_const(g, node_index, q):
    norm_const = 0
    for v_index in g.nodes_iter():
        if v_index == node_index:
            continue

        d = grid_distance(node_index, v_index)
        norm_const += pow(d, -q)
    return norm_const


def grid_distance(u, v):
    # u, v must be 2-tuples of x, y coords in grid
    # Just take manhatten distance
    return abs(u[0] - v[0]) + abs(u[1] - v[1])
