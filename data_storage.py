import os
import json


REPEAT_RESULT_FILENAME = "repeat_results.csv"

SIMULATION_INFO_FILENAME = "sim_info.json"
SHOW_MODEL_INFO_FILENAME = "show_info.json"
SHARE_MODEL_INFO_FILENAME = "share_info.json"
GRAPH_GENERATOR_INFO_FILENAME = "graph_gen_info.json"
GRAPH_EDGES_FILENAME = "graph.txt"
MESSAGES_FILENAME = "messages.txt"

DELIVERED_FILENAME = "delivered.txt"

SHOWN_MESSAGES_FILENAME = "shown.txt"
SHARED_MESSAGES_FILENAME = "shared.txt"


def write_repeat_result(path, total, delivered):
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
        f_show.write(json.dumps(sim.show_model.__dict__))
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
        for m in sim.messages:
            if m.delivered:
                f_del.write("{}:{}\n".format(m.id, m.delivery_turn))


def store_round_info(path, sim, round_no):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
    # shown messages
    with open(os.path.join(path, SHOWN_MESSAGES_FILENAME), 'w') as f_shown:
        for node_index in sim.g.nodes_iter():
            f_shown.write(str(node_index) + ":")
            f_shown.write(",".join(
                [str(m.id) for m in sim.g.node[node_index]['seen'][round_no]]))
            f_shown.write("\n")

    # shared messages
    with open(os.path.join(path, SHARED_MESSAGES_FILENAME), 'w') as f_shared:
        for node_index in sim.g.nodes_iter():
            f_shared.write(str(node_index) + ":")
            f_shared.write(",".join(
                [str(m.id) for m in sim.g.node[node_index]['shared'][round_no]]))
            f_shared.write("\n")
