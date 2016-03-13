import os
import json


GRAPH_DATA_FILENAME = "graph_data.csv"

REPEAT_RESULT_FILENAME = "repeat_results.csv"

SIMULATION_INFO_FILENAME = "sim_info.json"
SHOW_MODEL_INFO_FILENAME = "show_info.json"
DISTANCE_MEASURE_INFO_FILENAME = "distance_measure.json"
SHARE_MODEL_INFO_FILENAME = "share_info.json"
GRAPH_GENERATOR_INFO_FILENAME = "graph_gen_info.json"
GRAPH_EDGES_FILENAME = "graph.txt"
MESSAGES_FILENAME = "messages.txt"

DELIVERED_FILENAME = "delivered.txt"

SHOWN_MESSAGES_FILENAME = "shown.txt"
SHARED_MESSAGES_FILENAME = "shared.txt"


def store_graph_data(path, avgs, mins, maxs, x_values, x_label, as_percent):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
    with open(os.path.join(path, GRAPH_DATA_FILENAME), 'w') as f:
        if as_percent:
            percent_str = "percent"
        else:
            percent_str = "absolute"

        f.write("average delivered ({0}), min delivered ({0}),"
                " max delivered ({0}), {1}\n".format(percent_str, x_label))

        for avg, minv, maxv, xval in zip(avgs, mins, maxs, x_values):
            f.write("{}, {}, {}, {}\n".format(avg, minv, maxv, xval))


def store_repeat_result(path, total, delivered):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
    with open(os.path.join(path, REPEAT_RESULT_FILENAME), 'a') as f:
        f.write("{},{}\n".format(total, delivered))


def store_sim_info(path, sim):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
    # simulation object
    with open(os.path.join(path, SIMULATION_INFO_FILENAME), 'w') as f_sim:
        # round count
        # width
        # height
        d = {
            "round_count": sim.round_count,
            "width": sim.width,
            "height": sim.height,
            "show_model": type(sim.show_model).__name__,
            "share_model": type(sim.share_model).__name__,
            "graph_generator": type(sim.graph_generator).__name__,
        }

        f_sim.write(json.dumps(d))

    # show_model
    with open(os.path.join(path, SHOW_MODEL_INFO_FILENAME), 'w') as f_show:
        # Deal with distance_measure
        d = dict(sim.show_model.__dict__)
        d["distance_measure"] = type(sim.show_model.distance_measure).__name__
        f_show.write(json.dumps(d))
    # distance_measure
    with open(os.path.join(path, DISTANCE_MEASURE_INFO_FILENAME), 'w') as f_d:
        f_d.write(json.dumps(sim.show_model.distance_measure.__dict__))
    # share_model
    with open(os.path.join(path, SHARE_MODEL_INFO_FILENAME), 'w') as f_share:
        f_share.write(json.dumps(sim.share_model.__dict__))
    # graph_generator
    with open(os.path.join(path, GRAPH_GENERATOR_INFO_FILENAME), 'w') as f_gg:
        f_gg.write(json.dumps(sim.graph_generator.__dict__))

    # graph
    with open(os.path.join(path, GRAPH_EDGES_FILENAME), 'w') as f_g:
        for edge in sim.g.edges_iter():
            f_g.write("{}-{}\n".format(edge[0], edge[1]))

    # messages
    with open(os.path.join(path, MESSAGES_FILENAME), 'w') as f_msgs:
        for m in sim.messages:
            f_msgs.write("{}:{}:{}\n".format(
                m.id, m.source, m.destination))


def store_post_sim_info(path, sim):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
    # messages
    with open(os.path.join(path, DELIVERED_FILENAME), 'w') as f_del:
        f_del.write("Rounds simulated:{}\n".format(sim.rounds_simulated))
        f_del.write("Messages delivered:\n")
        for m in sim.messages:
            if m.delivered:
                f_del.write("{}:{}\n".format(m.id, m.delivery_turn))

    # round info
    with open(os.path.join(path, "shown.txt"), "w") as f_shown:
        for round_no in range(sim.rounds_simulated):
            f_shown.write("***ROUND {}***\n".format(round_no))
            for node_index in sim.g.nodes_iter():
                f_shown.write(str(node_index) + ":")
                f_shown.write(",".join(
                    [str(m.id) for
                     (m, u) in sim.g.node[node_index]['seen_all'][round_no]]))
                f_shown.write("\n")

    with open(os.path.join(path, "shared.txt"), "w") as f_shared:
        for round_no in range(sim.rounds_simulated):
            f_shared.write("***ROUND {}***".format(round_no))
            for node_index in sim.g.nodes_iter():
                f_shared.write(str(node_index) + ":")
                f_shared.write(",".join(
                    [str(m.id) for
                     m in sim.g.node[node_index]['shared'][round_no]]))
                f_shared.write("\n")
