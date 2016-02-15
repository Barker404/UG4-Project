#!/usr/bin/env python

import showing
import sharing
import numpy as np
from graph import KleinbergGenerator
from output import plot_simulations
from simulation import Simulation

ROWS = 20
COLUMNS = 20
K = 1
Q = 2

ROUND_COUNT = 25
MESSAGE_COUNT = 100

DRAW = True
WATCHED_MESSAGE = 0
DRAW_LABELS = False


def main():

    seen_limit = 20

    sm_1 = showing.AnyCloserGridShowModel(seen_limit)
    sm_2 = showing.FurtherProbGridShowModel(seen_limit, 0.4)
    sm_3 = showing.FurtherProbGridShowModel(seen_limit, 0.6)
    sm_4 = showing.OnlyBestGridShowModel(seen_limit)
    sm_5 = showing.AnyCloserShowModel(seen_limit)
    sm_6 = showing.FurtherProbShowModel(seen_limit, 0.4)
    sm_7 = showing.FurtherProbShowModel(seen_limit, 0.6)
    sm_8 = showing.OnlyBestShowModel(seen_limit)
    show_models = [sm_1, sm_2, sm_3, sm_4, sm_5, sm_6, sm_7, sm_8]
    filenames = ["AnyCloserGrid.png",
                 "FurtherProbGrid40.png",
                 "FurtherProbGrid60.png",
                 "OnlyBestGrid.png",
                 "AnyCloser.png",
                 "FurtherProb40.png",
                 "FurtherProb60.png",
                 "OnlyBest.png"]

    for i in range(len(show_models)):
        standard_show_model_graph(
            show_models[i], seen_limit, "standard_output", filenames[i])


def standard_show_model_graph(show_model, seen_limit,
                              output_path, graph_filename):
    share_prob = 0.5
    repeats = 10

    xs = []
    sims = []
    share_model = sharing.ProbShareModel(seen_limit, share_prob)

    graph_generator = KleinbergGenerator(COLUMNS, ROWS, K, Q)

    for k in range(25, 400, 25):
        xs.append(k)
        simulation = Simulation(show_model, share_model,
                                graph_generator, ROUND_COUNT, k)
        sims.append(simulation)

    plot_simulations(sims, xs, "Message count", repeats, True,
                     output_path, graph_filename)


def test_messages_percent_absolute():
    # Basic user model
    seen_limit = 20
    share_limit = 5

    show_model = showing.AnyCloserGridShowModel(seen_limit)
    share_model = sharing.BasicShareModel(seen_limit, share_limit)
    graph_generator = KleinbergGenerator(COLUMNS, ROWS, K, Q)

    sims = []
    xs = []
    for i in range(4000, 6250, 250):
        xs.append(i)
        simulation = Simulation(show_model, share_model, graph_generator,
                                ROUND_COUNT, i)
        sims.append(simulation)

    repeats = 15

    plot_simulations(sims, xs, "Message count", repeats, True,
                     "report_out/percent_vs_absolute", "percent.png")

    plot_simulations(sims, xs, "Message count", repeats, False,
                     "report_out/percent_vs_absolute", "absolute.png")


def compare_user_models():
    seen_limit = 20
    share_limit = 5
    share_prob_1 = 0.5
    share_prob_2 = 0.25
    share_model_a = sharing.BasicShareModel(seen_limit, share_limit)
    share_model_b = sharing.ProbShareModel(seen_limit, share_prob_1)
    share_model_c = sharing.ProbShareModel(seen_limit, share_prob_2)
    share_models = [share_model_a, share_model_b, share_model_c]

    show_model_1 = showing.AnyCloserGridShowModel(seen_limit)
    show_model_2 = showing.FurtherProbGridShowModel(seen_limit, 0.4)
    show_model_3 = showing.FurtherProbGridShowModel(seen_limit, 0.6)
    show_model_4 = showing.OnlyBestGridShowModel(seen_limit)
    show_models = [show_model_1, show_model_2, show_model_3, show_model_4]
    graph_generator = KleinbergGenerator(COLUMNS, ROWS, K, Q)

    filenames_all = [
        [
            "BasicShare_Prob0.png",
            "BasicShare_Prob40.png",
            "BasicShare_Prob60.png",
            "BasicShare_OnlyBest.png"],
        [
            "Prob50Share_Prob0.png",
            "Prob50Share_Prob40.png",
            "Prob50Share_Prob60.png",
            "Prob50Share_OnlyBest.png"],
        [
            "Prob25Share_Prob0.png",
            "Prob25Share_Prob40.png",
            "Prob25Share_Prob60.png",
            "Prob25Share_OnlyBest.png"]
    ]

    repeats = 10

    for i in range(0, 3):
        for j in range(0, 4):
            xs = []
            sims = []
            for k in range(25, 400, 25):
                xs.append(k)
                simulation = Simulation(show_models[j], share_models[i],
                                        graph_generator, ROUND_COUNT, k)
                sims.append(simulation)

            plot_simulations(sims, xs, "Message count", repeats, True,
                             "report_out/user_models", filenames_all[i][j])


def not_closer_prob_graph():
    # Probabilistic user model
    seen_limit = 20
    share_prob = 0.5
    share_model = sharing.ProbShareModel(seen_limit, share_prob)
    graph_generator = KleinbergGenerator(COLUMNS, ROWS, K, Q)

    message_counts = [200, 400, 800]
    filenames = [
        "notCloserProb_200messages.png",
        "notCloserProb_400messages.png",
        "notCloserProb_800messages.png"
    ]

    repeats = 10

    for i in range(0, 3):
        xs = []
        sims = []
        for j in np.arange(0.1, 1.1, 0.1):
            show_model = showing.FurtherProbGridShowModel(seen_limit, j)

            xs.append(j)
            simulation = Simulation(show_model, share_model,
                                    graph_generator, ROUND_COUNT,
                                    message_counts[i])
            sims.append(simulation)

        plot_simulations(sims, xs, "Not Closer Show Probability", repeats,
                         True, "report_out/not_closer_prob", filenames[i])

if __name__ == "__main__":
    main()
