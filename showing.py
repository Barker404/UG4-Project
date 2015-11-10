#!/usr/bin/env python

from collections import Counter


def show_alg(possible):
    # Receives (node, message)

    messages = [x[0] for x in possible]

    counts = Counter(messages)
    top = counts.most_common(3)
    top_messages = [t[0] for t in top]

    return filter((lambda x: (not x[0].delivered) and (x[0] in top_messages)),
                  possible)
