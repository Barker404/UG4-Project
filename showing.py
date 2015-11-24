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

    def show_alg(self, node_index, possible):
        candidates = self.select_candidates(node_index, possible)
        return self.select_final(candidates)

    def select_candidates(self, node_index, possible):
        # return any that are closer
        # possible is (message, node_index) pairs
        return [p for p in possible if (
            grid_distance(p[1], p[0].destination) >
            grid_distance(node_index, p[0].destination))]

    def select_final(self, candidates):
        # Select the correct amount randomly
        return random.sample(candidates, min(self.max_shown, len(candidates)))


class FurtherProbShowModel(ShowModel):

    def __init__(self, max_shown=20, not_closer_prob=0.5):
        self.not_closer_prob = not_closer_prob

    def show_alg(self, node_index, possible):
        candidates = self.select_candidates(node_index, possible)
        return self.select_final(candidates)

    def candidates_closer_prob_others(self, node_index, possible):
        # If closer, return always
        # If not closer, return with given probability
        return [p for p in possible if (
            grid_distance(p[1], p[0].destination) >
            grid_distance(node_index, p[0].destination))
            or
            random.random() > self.not_closer_prob]

    def select_final(self, candidates):
        # Select the correct amount randomly
        return random.sample(candidates, min(self.max_shown, len(candidates)))
