#!/usr/bin/env python

import showing
import sharing
import numpy as np
import graph
import os
from output import plot_simulations, re_plot_results
from simulation import Simulation

ROWS = 20
COLUMNS = 20
K = 1
Q = 2


def main():
    test_show_models(
        25, 825, 25, 20, showing.GraphDistanceMeasure(),
        "graph_dist/all_show_models")


def standard_show_model_graph(show_model, seen_limit,
                              output_path, graph_filename,
                              max_messages=400, message_step=25):
    share_prob = 0.5
    repeats = 20

    xs = []
    sims = []
    share_model = sharing.ProbShareModel(seen_limit, share_prob)

    graph_generator = graph.KleinbergGenerator(COLUMNS, ROWS, K, Q)

    for k in range(message_step, max_messages + message_step, message_step):
        xs.append(k)
        simulation = Simulation(show_model, share_model,
                                graph_generator, None, k)
        sims.append(simulation)

    plot_simulations(sims, xs, "Message count", repeats, True,
                     output_path, graph_filename)


def test_messages_percent_absolute():
    # Basic user model
    seen_limit = 20
    share_limit = 5

    grid_distance = showing.GridDistanceMeasure()

    show_model = showing.AnyCloserShowModel(seen_limit, grid_distance)
    share_model = sharing.BasicShareModel(seen_limit, share_limit)
    graph_generator = graph.KleinbergGenerator(COLUMNS, ROWS, K, Q)

    sims = []
    xs = []
    for i in range(4000, 6250, 250):
        xs.append(i)
        simulation = Simulation(show_model, share_model, graph_generator,
                                None, i)
        sims.append(simulation)

    repeats = 20

    plot_simulations(sims, xs, "Message count", repeats, True,
                     "report_out/percent_vs_absolute", "percent.png")

    plot_simulations(sims, xs, "Message count", repeats, False,
                     "report_out/percent_vs_absolute", "absolute.png")


def test_graph_sizes(start=5, end=55, step=5, repeats=20):
    seen_limit = 20
    further_prob = 0.5
    share_prob = 0.5

    # Grid distance measure
    # Any closer
    # Prob share
    distance_measure_a = showing.GridDistanceMeasure()
    show_model_a = showing.AnyCloserShowModel(
        seen_limit, distance_measure_a)
    share_model = sharing.ProbShareModel(seen_limit, share_prob)
    for size in range(start, end, step):
        graph_generator = graph.KleinbergGenerator(size, size, K, Q)
        simulation = Simulation(show_model_a, share_model, graph_generator,
                                round_count=None, message_count=size*size)
        simulation.repeat_simulation(repeats, as_percent=True,
                                     output_path=os.path.join(
                                        "out/graph_size/a", str(size)),
                                     store_data=True)
        print "Done a: {}".format(size)

    re_plot_results("Width and height of grid", True, as_percent=True,
                    output_path="out/graph_size/a", store_data=True)

    # Graph distance measure
    distance_measure_b = showing.GraphDistanceMeasure()
    show_model_b = showing.AnyCloserShowModel(
        seen_limit, distance_measure_b)
    for size in range(start, end, step):
        graph_generator = graph.KleinbergGenerator(size, size, K, Q)
        simulation = Simulation(show_model_b, share_model, graph_generator,
                                round_count=None, message_count=size*size)
        simulation.repeat_simulation(repeats, as_percent=True,
                                     output_path=os.path.join(
                                        "out/graph_size/b", str(size)),
                                     store_data=True)
        print "Done b: {}".format(size)

    re_plot_results("Width and height of grid", True, as_percent=True,
                    output_path="out/graph_size/b", store_data=True)

    # Grid distance measure
    # Further prob, p = 0.5
    show_model_c = showing.FurtherProbShowModel(
        seen_limit, further_prob, distance_measure_a)
    for size in range(start, end, step):
        graph_generator = graph.KleinbergGenerator(size, size, K, Q)
        simulation = Simulation(show_model_c, share_model, graph_generator,
                                round_count=None, message_count=size*size)
        simulation.repeat_simulation(repeats, as_percent=True,
                                     output_path=os.path.join(
                                        "out/graph_size/c", str(size)),
                                     store_data=True)
        print "Done c: {}".format(size)

    re_plot_results("Width and height of grid", True, as_percent=True,
                    output_path="out/graph_size/c", store_data=True)

    # Graph distance measure
    # Further prob, p = 0.5
    show_model_d = showing.FurtherProbShowModel(
        seen_limit, further_prob, distance_measure_b)
    for size in range(start, end, step):
        graph_generator = graph.KleinbergGenerator(size, size, K, Q)
        simulation = Simulation(show_model_d, share_model, graph_generator,
                                round_count=None, message_count=size*size)
        simulation.repeat_simulation(repeats, as_percent=True,
                                     output_path=os.path.join(
                                        "out/graph_size/d", str(size)),
                                     store_data=True)
        print "Done d: {}".format(size)

    re_plot_results("Width and height of grid", True, as_percent=True,
                    output_path="out/graph_size/d", store_data=True)


def compare_user_models(msg_count_start=25, msg_count_end=825,
                        msg_count_step=25, repeats=20):
    seen_limit = 20
    share_limit = 5
    share_prob_1 = 0.5

    share_model_a = sharing.BasicShareModel(seen_limit, share_limit)
    share_model_b = sharing.ProbShareModel(seen_limit, share_prob_1)
    share_models = [share_model_a, share_model_b]

    grid_distance = showing.GridDistanceMeasure()

    show_model_1 = showing.AnyCloserShowModel(seen_limit, grid_distance)
    show_model_2 = showing.FurtherProbShowModel(seen_limit, 0.4, grid_distance)
    show_model_3 = showing.FurtherProbShowModel(seen_limit, 0.6, grid_distance)
    show_model_4 = showing.OnlyBestShowModel(seen_limit, grid_distance)
    show_models = [show_model_1, show_model_2, show_model_3, show_model_4]

    graph_generator = graph.KleinbergGenerator(COLUMNS, ROWS, K, Q)

    subdirs_all = [
        [
            "BasicShare_Prob0",
            "BasicShare_Prob40",
            "BasicShare_Prob60",
            "BasicShare_OnlyBest"],
        [
            "ProbShare_Prob0",
            "ProbShare_Prob40",
            "ProbShare_Prob60",
            "ProbShare_OnlyBest"]
    ]

    for i in range(0, 2):
        for j in range(0, 4):
            xs = []
            sims = []
            for k in range(msg_count_start, msg_count_end, msg_count_step):
                xs.append(k)
                simulation = Simulation(show_models[j], share_models[i],
                                        graph_generator, round_count=None,
                                        message_count=k)
                sims.append(simulation)

            plot_simulations(
                sims, xs, "Message count", repeats, as_percent=True,
                output_path=os.path.join("out/user_models", subdirs_all[i][j]),
                store_data=True)

            # re_plot_results(
            #     "Message count", True, as_percent=True,
            #     output_path=os.path.join("out/user_models", subdirs_all[i][j]))


def test_not_closer_prob(msg_count_start=200, msg_count_end=1000,
                         msg_count_step=200, step=0.05, repeats=20,
                         distance_measure=None, dir="not_closer_prob"):
    # Probabilistic user model
    if distance_measure is None:
        distance_measure = showing.GridDistanceMeasure()

    seen_limit = 20
    share_prob = 0.5
    share_model = sharing.ProbShareModel(seen_limit, share_prob)
    graph_generator = graph.KleinbergGenerator(COLUMNS, ROWS, K, Q)

    for i in range(msg_count_start, msg_count_end, msg_count_step):
        xs = []
        sims = []
        for j in np.arange(0.0, 1.0 + step, step):
            show_model = showing.FurtherProbShowModel(
                seen_limit, j, distance_measure)

            xs.append(j)
            simulation = Simulation(show_model, share_model,
                                    graph_generator, round_count=None,
                                    message_count=i)
            sims.append(simulation)

            # simulation.repeat_simulation(
            #     repeats, as_percent=True,
            #     output_path=os.path.join(
            #         "out/not_closer_prob",
            #         "notCloserProb_{}messages".format(i),
            #         str(j)),
            #     store_data=True)

        # re_plot_results(
        #     "Not Closer Show Probability", True, as_percent=True,
        #     output_path=os.path.join(
        #         "out/not_closer_prob",
        #         "notCloserProb_{}messages".format(i)),
        #     store_data=True)

        plot_simulations(
            sims, xs, "Not Closer Show Probability", repeats, as_percent=True,
            output_path=os.path.join(
                "out/{}".format(dir),
                "notCloserProb_{}messages".format(i)),
            store_data=True)


def test_distance_priority_fraction(
    msg_count_start=200, msg_count_end=1000, msg_count_step=200, step=0.05,
        repeats=20, distance_measure=None, dir="distance_priority_fraction"):
    # Probabilistic user model
    if distance_measure is None:
        distance_measure = showing.GridDistanceMeasure()

    seen_limit = 20
    share_prob = 0.5
    share_model = sharing.ProbShareModel(seen_limit, share_prob)
    graph_generator = graph.KleinbergGenerator(COLUMNS, ROWS, K, Q)

    for i in range(msg_count_start, msg_count_end, msg_count_step):
        xs = []
        sims = []
        for j in np.arange(0.0, 1.0 + step, step):
            show_model = showing.FractionalDistancePriorityShowModel(
                seen_limit, j, distance_measure)

            xs.append(j)
            simulation = Simulation(show_model, share_model,
                                    graph_generator, round_count=None,
                                    message_count=i)
            sims.append(simulation)

        plot_simulations(
            sims, xs, "Distance Priority Fraction", repeats, as_percent=True,
            output_path=os.path.join(
                "out/{}".format(dir),
                "distancePriorityFraction_{}messages".format(i)),
            store_data=True)


def test_show_models(msg_count_start=25, msg_count_end=825,
                     msg_count_step=25, repeats=20,
                     distance_measure=None, dir="all_show_models"):
    if distance_measure is None:
        distance_measure = showing.GridDistanceMeasure()

    seen_limit = 20
    share_prob = 0.5
    share_model = sharing.ProbShareModel(seen_limit, share_prob)
    graph_generator = graph.KleinbergGenerator(COLUMNS, ROWS, K, Q)

    models = [
        showing.AnyCloserShowModel(
            seen_limit, distance_measure),
        showing.FurtherProbShowModel(
            seen_limit, 0.2, distance_measure),
        showing.FurtherProbShowModel(
            seen_limit, 0.4, distance_measure),
        showing.OnlyBestShowModel(
            seen_limit, distance_measure),
        showing.DistancePriorityShowModel(
            seen_limit, distance_measure),
        showing.FractionalDistancePriorityShowModel(
            seen_limit, 0.05, distance_measure),
        showing.FractionalDistancePriorityShowModel(
            seen_limit, 0.2, distance_measure),
    ]
    subdirs = [
        "AnyCloser",
        "FurtherProb_20",
        "FurtherProb_40",
        "OnlyBest",
        "DistancePriority",
        "FractionalDistancePriority_05",
        "FractionalDistancePriority_20"
    ]

    for i in range(0, len(subdirs)):
        xs = []
        sims = []
        show_model = models[i]
        for j in range(msg_count_start, msg_count_end, msg_count_step):
            xs.append(j)
            simulation = Simulation(show_model, share_model,
                                    graph_generator, round_count=None,
                                    message_count=j)
            sims.append(simulation)

        #     simulation.repeat_simulation(
        #         repeats, as_percent=True,
        #         output_path=os.path.join(
        #             "out/all_show_models", subdirs[i], str(j)),
        #         store_data=True)

        # re_plot_results(
        #     "Message Count", True, as_percent=True,
        #     output_path=os.path.join("out/all_show_models", subdirs[i]),
        #     store_data=True)

        plot_simulations(
            sims, xs, "Message Count", repeats, as_percent=True,
            output_path=os.path.join("out/{}".format(dir), subdirs[i]),
            store_data=True)

if __name__ == "__main__":
    main()
