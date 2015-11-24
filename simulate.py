#!/usr/bin/env python

import showing
import sharing
from output import draw_graph
from graph import kleinberg
from message import Message
import random

ROWS = 30
COLUMNS = 30
K = 1
Q = 2

ROUND_COUNT = 10
MESSAGE_COUNT = 200

DRAW = True
WATCHED_MESSAGE = 0
DRAW_LABELS = False


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

    def run_simulation(self, draw_output, watched_message, draw_labels):

        if draw_output:
            # Draw initial config
            draw_graph(self.g, self.pos, 0, self.messages,
                       self.show_model.max_shown, watched_message, draw_labels)

        # Simulate rounds
        for round_no in range(1, self.round_count + 1):
            print "ROUND {0}".format(round_no)
            for node_index in self.g.nodes_iter():

                # Get messages that could possibly be shown
                # possible, seen and shared have format
                # [(message, previous_node)]
                possible = [(message, neighbour)
                            for neighbour in self.g.neighbors_iter(node_index)
                            for message in self.g.node[neighbour]['shared']
                            [round_no - 1]]

                # Update messages
                showResults = self.show_model.show_alg(node_index, possible)
                seen = list(set([s[0] for s in showResults]))

                self.g.node[node_index]['seen'].append(seen)
                for message in self.g.node[node_index]['seen'][round_no]:
                    if (message.destination == node_index and
                            not message.delivered):
                        message.delivered = True
                        print str(message.id) + " delivered!"

                shareResult = self.share_model.share_alg(showResults)

                self.g.node[node_index]['shared'].append(shareResult)

            if draw_output:
                draw_graph(self.g, self.pos, round_no, self.messages,
                           self.show_model.max_shown, watched_message,
                           draw_labels)

        return len([x for x in self.messages if x.delivered])


def main():
    show_model = showing.AnyCloserShowModel(20)
    share_model = sharing.BasicShareModel(5)

    simulation = Simulation(show_model, share_model,
                            ROWS, COLUMNS, K, Q,
                            ROUND_COUNT, MESSAGE_COUNT)

    delivered = simulation.run_simulation(DRAW, WATCHED_MESSAGE, DRAW_LABELS)

    print "{0} delivered out of {1}".format(delivered, MESSAGE_COUNT)

if __name__ == "__main__":
    main()
