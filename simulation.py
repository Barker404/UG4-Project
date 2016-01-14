#!/usr/bin/env python

from output import Visualiser
from graph import kleinberg
from message import Message
import random


class Simulation(object):

    def __init__(self, show_model, share_model,
                 rows=30, columns=30, k=1, q=2,
                 round_count=10, message_count=50):
        self.show_model = show_model
        self.share_model = share_model
        self.rows = rows
        self.columns = columns
        self.k = k
        self.q = q
        self.round_count = round_count
        self.message_count = message_count

        self.generate_graph()
        self.generate_messages()

    def generate_graph(self):
        # Create graph
        self.g = kleinberg(self.rows, self.columns, self.k, self.q)
        self.pos = dict(zip(self.g, self.g))
        print "made graph"

        # Set up node attributes
        self.clear_simulation()

        return (self.g, self.pos)

    def generate_messages(self):
        self.messages = []

        for i in range(0, self.message_count):
            source_index = random.choice(self.g.nodes())
            destination_index = random.choice(self.g.nodes())
            message = Message(i, source_index, destination_index)
            self.messages.append(message)

            # Assume starting node always shares
            self.g.node[source_index]['seen'][0].append(message)
            self.g.node[source_index]['shared'][0].append(message)

        return self.messages

    def clear_simulation(self):
        for i in self.g.nodes_iter():
            self.g.node[i]['seen'] = [[]]
            self.g.node[i]['shared'] = [[]]

    def run_simulation(self, output_images, output_video, watched_message,
                       draw_labels, as_percent=False):

        self.visualiser = Visualiser(self.columns, self.rows)

        if output_images:
            # Draw round 0
            self.visualiser.draw_image(
                self.g, self.pos, 0, self.messages, self.show_model.max_shown,
                watched_message, draw_labels)

        # Simulate rounds
        for round_no in range(1, self.round_count + 1):
            self.simulate_round(round_no, output_images,
                                watched_message, draw_labels)

        if output_video:
            self.visualiser.create_video(
                self.g, self.pos, self.round_count, self.messages,
                self.show_model.max_shown, watched_message, draw_labels)

        num_delivered = len([x for x in self.messages if x.delivered])
        if as_percent:
            return 100 * float(num_delivered) / float(self.message_count)
        else:
            return num_delivered

    def simulate_round(self, round_no, output_images, watched_message,
                       draw_labels):
        print "ROUND {0}".format(round_no)
        for node_index in self.g.nodes_iter():

            # Get messages that could possibly be shown
            # possible, seen and shared have format
            # [(message, previous_node)]
            possible = [(message, neighbour)
                        for neighbour in self.g.neighbors_iter(node_index)
                        for message in self.g.node[neighbour]['shared']
                        [round_no - 1]]

            # Update seen messages
            showResults = self.show_model.show_alg(
                self.g, node_index, possible)
            seen = list(set([s[0] for s in showResults]))
            self.g.node[node_index]['seen'].append(seen)

            # Check if messages have reached destinations
            for message in self.g.node[node_index]['seen'][round_no]:
                if (message.destination == node_index and
                        not message.delivered):
                    message.delivered = True
                    message.delivery_turn = round_no
                    print str(message.id) + " delivered!"

            # Update shared messages
            shareResult = self.share_model.share_alg(showResults)
            self.g.node[node_index]['shared'].append(shareResult)

        if output_images:
            self.visualiser.draw_image(
                self.g, self.pos, round_no, self.messages,
                self.show_model.max_shown, watched_message, draw_labels)

    def repeat_simulation(self, count, regenerate_graph=True,
                          regenerate_messages=True, as_percent=False):
        total = 0
        total_delivered = 0
        min_delivered = float('inf')
        max_delivered = 0
        for i in range(count):
            self.clear_simulation()
            if regenerate_graph or i == 0:
                self.generate_graph()
            if regenerate_messages or i == 0:
                self.generate_messages()

            delivered = self.run_simulation(False, False, None, False)

            total += self.message_count
            total_delivered += delivered
            if delivered < min_delivered:
                min_delivered = delivered
            if delivered > max_delivered:
                max_delivered = delivered

            print "Finished simulation {} of {}".format(i + 1, count)

        total_messages = count * self.message_count
        print "Delivered a total of {} out of {} - {}%".format(
            total_delivered, total_messages,
            100 * float(total_delivered) / float(total_messages))
        print "Min: {} out of {} - {}%".format(
            min_delivered, self.message_count,
            100 * float(min_delivered) / float(self.message_count))
        print "Max: {} out of {} - {}%".format(
            max_delivered, self.message_count,
            100 * float(max_delivered) / float(self.message_count))

        if as_percent:
            return (100 * float(total_delivered) / float(total_messages),
                    100 * float(min_delivered) / float(self.message_count),
                    100 * float(max_delivered) / float(self.message_count))
        else:
            return (total_delivered, min_delivered, max_delivered)
