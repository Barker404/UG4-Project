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

ROUND_COUNT = 25
MESSAGE_COUNT = 100

DRAW = True
WATCHED_MESSAGE = 0
DRAW_LABELS = False


def main():
    compare_user_models()


def test_messages_percent_absolute():
    # Basic user model
    seen_limit = 20
    share_limit = 5

    show_model = showing.AnyCloserShowModel(seen_limit)
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
    # Basic user model
    seen_limit = 20
    share_limit = 5
    share_prob_1 = 0.5
    share_prob_2 = 0.25
    share_model_a = sharing.BasicShareModel(seen_limit, share_limit)
    share_model_b = sharing.ProbShareModel(seen_limit, share_prob_1)
    share_model_c = sharing.ProbShareModel(seen_limit, share_prob_2)
    share_models = [share_model_a, share_model_b, share_model_c]

    show_model_1 = showing.AnyCloserShowModel(seen_limit)
    show_model_2 = showing.FurtherProbShowModel(seen_limit, 0.4)
    show_model_3 = showing.FurtherProbShowModel(seen_limit, 0.6)
    show_model_4 = showing.OnlyBestShowModel(seen_limit)
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

if __name__ == "__main__":
    main()
