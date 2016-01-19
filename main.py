#!/usr/bin/env python

import showing
import sharing
from graph import KleinbergGenerator
from output import plot_simulations
from simulation import Simulation

ROWS = 20
COLUMNS = 20
K = 1
Q = 2

ROUND_COUNT = 20
MESSAGE_COUNT = 100

DRAW = True
WATCHED_MESSAGE = 0
DRAW_LABELS = False


def main():
    show_model = showing.AnyCloserShowModel(20)
    share_model = sharing.BasicShareModel(20, 5)
    graph_generator = KleinbergGenerator(COLUMNS, ROWS, K, Q)

    simulation = Simulation(show_model, share_model, graph_generator,
                            ROUND_COUNT, MESSAGE_COUNT)
    simulation.repeat_simulation(1)

if __name__ == "__main__":
    main()
