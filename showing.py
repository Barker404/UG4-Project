#!/usr/bin/env python

from collections import Counter


def show_alg(possible):
    # Receives (node, message)

    messages = [x[0] for x in possible if not x[0].delivered]

    counts = Counter(messages)
    top = counts.most_common(3)
    top_messages = [t[0] for t in top]

    return top_messages
