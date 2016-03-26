#!/usr/bin/env python

import os
from output import Visualiser
from message import Message
import random
import data_storage
from datetime import datetime


class Simulation(object):

    def __init__(self, show_model, share_model, graph_generator,
                 round_count=10, message_count=50, pregenerate_graph=False):
        self.show_model = show_model
        self.share_model = share_model
        self.graph_generator = graph_generator
        self.round_count = round_count
        self.message_count = message_count

        if pregenerate_graph:
            self.generate_graph()
            self.generate_messages()
        else:
            self.g = None

    def generate_graph(self, generate_pos=True):
        # Create graph
        self.g, self.g_info = self.graph_generator.generate_graph()
        if generate_pos:
            self.pos = self.graph_generator.generate_positions(self.g)

            self.width = self.graph_generator.get_width(self.g)
            self.height = self.graph_generator.get_height(self.g)

        print "made graph"

        # Set up node attributes
        self.clear_simulation()

        if generate_pos:
            return (self.g, self.pos)
        else:
            return (self.g, None)

    def generate_messages(self):
        self.messages = []

        for i in range(0, self.message_count):
            source_index = random.choice(self.g.nodes())
            destination_index = random.choice(self.g.nodes())
            message = Message(i, source_index, destination_index)
            self.messages.append(message)

            # Assume starting node always shares
            self.g.node[source_index]['seen'][0].append(message)
            self.g.node[source_index]['seen_all'][0].append(
                (message, source_index))
            self.g.node[source_index]['shared'][0].append(message)

        return self.messages

    def clear_simulation(self):
        if self.g is not None:
            for i in self.g.nodes_iter():
                self.g.node[i]['seen'] = [[]]
                self.g.node[i]['seen_all'] = [[]]
                self.g.node[i]['shared'] = [[]]

    def run_simulation(self, output_images, output_video, output_path='output',
                       watched_message=0, draw_labels=False, as_percent=False,
                       store_data=False):
        if store_data:
            data_storage.store_sim_info(output_path, self)

        if output_images or output_video:
            visualiser_path = os.path.join(output_path, "visualisation")
            self.visualiser = Visualiser(
                self.width, self.height, visualiser_path)

        if output_images:
            # Draw round 0
            self.visualiser.draw_image(
                self.g, self.pos, 0, self.messages, self.show_model.max_shown,
                watched_message, draw_labels)

        # Simulate rounds
        round_no = 0
        simulating = True
        while simulating:
            round_no += 1
            self.simulate_round(round_no, output_images,
                                watched_message, draw_labels)

            if self.round_count is not None:
                simulating = not round_no >= self.round_count
            else:
                # Check if all message propogation has ended
                any_seen = any([self.g.node[n]['seen'][round_no]
                                for n in self.g.nodes_iter()])
                simulating = (any_seen and
                              round_no <= self.g.number_of_nodes() * 2)

        # Will be the same as round_count if it is not None
        self.rounds_simulated = round_no

        if output_video:
            self.visualiser.create_video(
                self.g, self.pos, self.rounds_simulated, self.messages,
                self.show_model.max_shown, watched_message, draw_labels)

        if store_data:
            data_storage.store_post_sim_info(output_path, self)
        num_delivered = len([x for x in self.messages if x.delivered])

        if output_images or output_video:
            self.visualiser.clear()

        if as_percent:
            return 100 * float(num_delivered) / float(self.message_count)
        else:
            return num_delivered

    def simulate_round(self, round_no, output_images, watched_message,
                       draw_labels):
        # print "ROUND {0}".format(round_no)
        for node_index in self.g.nodes_iter():

            # Get messages that could possibly be shown
            # possible, seen and shared have format
            # [(message, previous_node)]
            possible = [(message, neighbour)
                        for neighbour in self.g.neighbors_iter(node_index)
                        for message in self.g.node[neighbour]['shared']
                        [round_no - 1]]

            # Update seen messages
            show_result = self.show_model.show_alg(
                self.g, self.g_info, node_index, possible)
            self.g.node[node_index]['seen_all'].append(show_result)
            seen = list(set([s[0] for s in show_result]))
            self.g.node[node_index]['seen'].append(seen)

            # Check if messages have reached destinations
            for message in self.g.node[node_index]['seen'][round_no]:
                if (message.destination == node_index and
                        not message.delivered):
                    message.delivered = True
                    message.delivery_turn = round_no
                    # print str(message.id) + " delivered!"

            # Update shared messages
            share_result = self.share_model.share_alg(show_result)
            self.g.node[node_index]['shared'].append(share_result)

        if output_images:
            self.visualiser.draw_image(
                self.g, self.pos, round_no, self.messages,
                self.show_model.max_shown, watched_message, draw_labels)

    def repeat_simulation(self, count, regenerate_graph=True,
                          regenerate_messages=True, as_percent=False,
                          output_graphs=False, output_videos=False,
                          output_path='output', watched_message=0,
                          draw_labels=False, store_data=False,
                          store_less_data=False):
        total = 0
        total_delivered = 0
        min_delivered = float('inf')
        max_delivered = 0
        for i in range(count):

            self.clear_simulation()
            if regenerate_graph:
                self.generate_graph(output_graphs or output_videos)
            if regenerate_messages:
                self.generate_messages()

            timestamp = datetime.now().strftime("%d%m%y-%H%M%S-%f")
            new_output_path = os.path.join(output_path, timestamp)
            delivered = self.run_simulation(output_graphs, output_videos,
                                            new_output_path, watched_message,
                                            draw_labels, as_percent=False,
                                            store_data=store_data)

            if store_data or store_less_data:
                data_storage.store_repeat_result(
                    output_path, self.message_count, delivered)

            total += self.message_count
            total_delivered += delivered
            if delivered < min_delivered:
                min_delivered = delivered
            if delivered > max_delivered:
                max_delivered = delivered

            print "Finished simulation {} of {}".format(i + 1, count)

        total_messages = count * self.message_count

        if as_percent:
            return (100 * float(total_delivered) / float(total_messages),
                    100 * float(min_delivered) / float(self.message_count),
                    100 * float(max_delivered) / float(self.message_count))
        else:
            return (total_delivered / count, min_delivered, max_delivered)
