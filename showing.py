#!/usr/bin/env python

import random
import heapq

from abc import ABCMeta, abstractmethod


class ShowModel(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def show_alg(self, g, node_index, possible):
        pass


class AnyCloserShowModel(ShowModel):

    def __init__(self, max_shown=20, distance_measure=None):
        self.max_shown = max_shown
        if distance_measure is None:
            distance_measure = GraphDistanceMeasure()
        self.distance_measure = distance_measure

    def show_alg(self, g, g_info, node_index, possible):
        candidates = self.select_candidates(g_info, node_index, possible)
        return self.select_final(candidates)

    def select_candidates(self, g_info, node_index, possible):
        # return any that are closer
        # possible is (message, node_index) pairs
        return [p for p in possible if (
            not p[0].delivered and
            self.distance_measure.distance(g_info, p[1], p[0].destination) >
            self.distance_measure.distance(
                g_info, node_index, p[0].destination))]

    def select_final(self, candidates):
        # Select the correct amount randomly
        return random.sample(candidates, min(self.max_shown, len(candidates)))


class FurtherProbShowModel(ShowModel):

    def __init__(self, max_shown=20, not_closer_prob=0.5,
                 distance_measure=None):
        self.not_closer_prob = not_closer_prob
        self.max_shown = max_shown
        if distance_measure is None:
            distance_measure = GraphDistanceMeasure()
        self.distance_measure = distance_measure

    def show_alg(self, g, g_info, node_index, possible):
        candidates = self.select_candidates(g_info, node_index, possible)
        return self.select_final(candidates)

    def select_candidates(self, g_info, node_index, possible):
        # If closer, return always
        # If not closer, return with given probability
        return [p for p in possible if (
            not p[0].delivered and
            (self.distance_measure.distance(g_info, p[1], p[0].destination) >
             self.distance_measure.distance(
                g_info, node_index, p[0].destination) or
             random.random() < self.not_closer_prob))]

    def select_final(self, candidates):
        # Select the correct amount randomly
        return random.sample(candidates, min(self.max_shown, len(candidates)))


class OnlyBestShowModel(ShowModel):

    def __init__(self, max_shown=20, distance_measure=None):
        self.max_shown = max_shown
        if distance_measure is None:
            distance_measure = GraphDistanceMeasure()
        self.distance_measure = distance_measure

    def show_alg(self, g, g_info, node_index, possible):
        # The first candidates
        return self.select_candidates(
            g, g_info, node_index, possible)[:self.max_shown]

    def select_candidates(self, g, g_info, node_index, possible):
        # Return only those messages for which this node is best
        return [p for p in possible if (
            not p[0].delivered and
            self.best_node(g, g_info, p[0], p[1]) == node_index)]

    def best_node(self, g, g_info, message, current_node_index):
        min_index = None
        min_distance = float('inf')

        for neighbour_index in g.neighbors_iter(current_node_index):
            distance = self.distance_measure.distance(
                g_info, neighbour_index, message.destination)

            # Ensure that we not only get the min, but always the same index
            # (in the case that distances are the same
            # - even if node iteration order changes)
            if distance < min_distance or (
                    distance == min_distance and neighbour_index < min_index):
                min_distance = distance
                min_index = neighbour_index

        return min_index


class DistancePriorityShowModel(ShowModel):

    def __init__(self, max_shown=20, distance_measure=None):
        self.max_shown = max_shown
        if distance_measure is None:
            distance_measure = GraphDistanceMeasure()
        self.distance_measure = distance_measure

    def show_alg(self, g, g_info, node_index, possible):
        possible_sorted = sorted(
            [p for p in possible if not p[0].delivered],
            key=lambda p: self.distance_measure.distance(
                g_info, node_index, p[0].destination))
        return possible_sorted[:self.max_shown]


class FractionalDistancePriorityShowModel(ShowModel):

    def __init__(self, max_shown=20, priority_fraction=0.75,
                 distance_measure=None):
        self.max_shown = max_shown
        self.priority_fraction = priority_fraction
        self.priority_max = int(priority_fraction * float(max_shown))
        self.extra_max = max_shown - self.priority_max
        if distance_measure is None:
            distance_measure = GraphDistanceMeasure()
        self.distance_measure = distance_measure

    def show_alg(self, g, g_info, node_index, possible):
        possible_sorted = sorted(
            [p for p in possible if not p[0].delivered],
            key=lambda p: self.distance_measure.distance(
                g_info, node_index, p[0].destination))
        chosen = possible_sorted[:self.priority_max]
        others = possible_sorted[self.priority_max:]
        chosen.extend(self.choose_extra(others))
        return chosen

    def choose_extra(self, candidates):
        extra_size = min(len(candidates), self.extra_max)
        chosen = random.sample(candidates, extra_size)
        return chosen


class DistanceMeasure(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def distance(self, g_info, u, v):
        pass


class GridDistanceMeasure(DistanceMeasure):
    def distance(self, g_info, u, v):
        return g_info.grid_distance(u, v)


class GraphDistanceMeasure(DistanceMeasure):
    def distance(self, g_info, u, v):
        return g_info.graph_distance(u, v)


class DiffusionDistanceMeasure(DistanceMeasure):
    def __init__(self, t):
        self.t = t

    def distance(self, g_info, u, v):
        return g_info.diffusion_distance(u, v, self.t)
