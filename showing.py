#!/usr/bin/env python

from collections import Counter
from graph import grid_distance
import random

from abc import ABCMeta, abstractmethod


class ShowModel(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def show_alg(self, g, node_index, possible):
        pass


class AnyCloserShowModel(ShowModel):

    def __init__(self, max_shown=20):
        self.max_shown = max_shown

    def show_alg(self, g, node_index, possible):
        candidates = self.select_candidates(node_index, possible)
        return self.select_final(candidates)

    def select_candidates(self, node_index, possible):
        # return any that are closer
        # possible is (message, node_index) pairs
        return [p for p in possible if (
            not p[0].delivered and
            grid_distance(p[1], p[0].destination) >
            grid_distance(node_index, p[0].destination))]

    def select_final(self, candidates):
        # Select the correct amount randomly
        return random.sample(candidates, min(self.max_shown, len(candidates)))


class FurtherProbShowModel(ShowModel):

    def __init__(self, max_shown=20, not_closer_prob=0.5):
        self.not_closer_prob = not_closer_prob
        self.max_shown = max_shown

    def show_alg(self, g, node_index, possible):
        candidates = self.select_candidates(node_index, possible)
        return self.select_final(candidates)

    def select_candidates(self, node_index, possible):
        # If closer, return always
        # If not closer, return with given probability
        return [p for p in possible if (
            not p[0].delivered and
            (grid_distance(p[1], p[0].destination) >
             grid_distance(node_index, p[0].destination) or
             random.random() > self.not_closer_prob))]

    def select_final(self, candidates):
        # Select the correct amount randomly
        return random.sample(candidates, min(self.max_shown, len(candidates)))


class OnlyBestShowModel(ShowModel):

    def __init__(self, max_shown=20):
        self.max_shown = max_shown

    def show_alg(self, g, node_index, possible):
        # The first candidates
        return self.select_candidates(g, node_index, possible)[:self.max_shown]

    def select_candidates(self, g, node_index, possible):
        # Return only those messages for which this node is best
        return [p for p in possible if (
            self.best_node(g, p[0], p[1]) == node_index)]

    def best_node(self, g, message, current_node_index):
        min_index = None
        min_distance = float('inf')

        for neighbour_index in g.neighbors_iter(current_node_index):
            distance = grid_distance(neighbour_index, message.destination)

            # Ensure that we not only get the min, but always the same index
            # (in the case that distances are the same
            # - even if node iteration order changes)
            if distance < min_distance or (
                    distance == min_distance and neighbour_index < min_index):
                min_distance = distance
                min_index = neighbour_index

        return min_index
