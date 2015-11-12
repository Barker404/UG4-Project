#!/usr/bin/env python

from collections import Counter
from graph import grid_distance

MAX_SHOWN = 3


def show_alg(g, node_index, possible):
    # Receives (node, message)
    candidates = select_candidates(g, node_index, possible)
    return select_final(g, node_index, candidates)


def select_candidates(g, node_index, possible):
    return candidates_any_closer(g, node_index, possible)


def candidates_any_closer(g, node_index, possible):
    return [p for p in possible if (
        grid_distance(p[1], p[0].destination) >
        grid_distance(node_index, p[0].destination))]


def candidates_distance_prob(g, node_index, possible):
    # Todo: make this less unoptimised
    pass


def select_final(g, node_index, candidates):
    messages = [x[0] for x in candidates if not x[0].delivered]

    counts = Counter(messages)
    top = counts.most_common(MAX_SHOWN)
    top_messages = [t[0] for t in top]

    return top_messages
