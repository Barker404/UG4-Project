#!/usr/bin/env python

import timeit
import graph


print(timeit.timeit("graph.kleinberg(70, 70, 1, 2)",
                    setup="import graph", number=2))

print(timeit.timeit("graph.kleinberg2(70, 70, 1, 2)",
                    setup="import graph", number=2))

print(timeit.timeit("graph.kleinberg3(70, 70, 1, 2)",
                    setup="import graph", number=2))
