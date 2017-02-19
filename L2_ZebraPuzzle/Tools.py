
"""
===========================================================================
1. compute runtime of a function call
"""
import time

def timecall(fn, *args):
    """
    return execution time of fn
    """
    t0 = time.clock()
    res = fn(*args)
    t1 = time.clock()
    return t1-t0, res


"""
===========================================================================
1. count number of executions in for loops
"""

def c(sequence):
    """
    c.starts and c.items are attributes of c()
    """
    c.starts += 1 # starts is number of starts
    for item in sequence:
        c.items += 1 # items is number of step after start
        yield item


def instrument_fn(fn, *args):
    """
    count number of execution
    """
    c.starts, c.items = 0, 0
    result = fn(*args)
    print '%s got %s with %5d iters over %7d items' % (fn.__name__, result, c.starts, c.items)