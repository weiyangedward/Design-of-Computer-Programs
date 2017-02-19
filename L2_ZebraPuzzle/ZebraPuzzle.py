import itertools

"""
===========================================================================
1. imright(h1, h2) -> True if h1 = h2 + 1
2. nextto(h1, h2) -> True if abs(h1-h2) == 1
"""
# ----------------
# User Instructions
#
# Add the appropriate return statement to the nextto(h1, h2)
# function below. It should return True when two houses
# differ by 1, otherwise it should return False.

def imright(h1, h2):
    """
    true if house1 is immediately to the right of house2
    """
    return h1-h2 == 1

def nextto(h1, h2):
    """
    true if two houses are next to each other
    """
    return abs(h1-h2) == 1


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

"""
===========================================================================
1. zebra_puzzle() -> answer to puzzle
"""
def zebra_puzzle():
    """
    return a tuple (WATER, ZEBRA) indicating their house numbers

    Tricks to run faster:
    move 'if' constraint up before the 'for' loop to remove redundancy/prune branches
    """
    houses = first, _, middle, _, _ = [1,2,3,4,5]
    orderings = list(itertools.permutations(houses))
    return next((WATER, ZEBRA)
        for (red, green, ivory, yellow, blue) in c(orderings)
        if (imright(green, ivory))      #6
        for (Englishman, Spaniard, Ukrainian, Japanese, Norwegian) in c(orderings)
        if (Englishman == red)          #2, move up to remove redundancy
        if (Norwegian == first)         #10
        if (nextto(Norwegian, blue))    #15
        for (coffee, tea, milk, oj, WATER) in c(orderings)
        if (coffee == green)            #4
        if (Ukrainian == tea)           #5
        if (milk == middle)             #9
        for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in c(orderings)
        if (Kools == yellow)            #8
        if (LuckyStrike == oj)          #13
        if (Japanese == Parliaments)    #14
        for (dog, snails, fox, horse, ZEBRA) in c(orderings)
        if (Spaniard == dog)            #3
        if (OldGold == snails)          #7
        if (nextto(Chesterfields,fox))  #11
        if (nextto(Kools, horse))       #12
        )

instrument_fn(zebra_puzzle) # count how many executions

"""
===========================================================================
1. tools: timecall()
"""
import time

def timecall(fn, *args):
    """
    '*args' can take any number of arguments as tuple 'args'

    def sth(fn, *args):
        fn(*args)

    if: sth(f, 1,2,3)
    then: *args = (1,2,3)

    fn(*args) will un-pack tuple (1,2,3), so fn(*args) == fn(1,2,3)
    where (args) will use (1,2,3) as a single argument
    """
    t0 = time.clock()
    res = fn(*args)
    t1 = time.clock()
    return t1-t0, res


# ----------------
# User Instructions
#
# Modify the timedcalls(n, fn, *args) function so that it calls
# fn(*args) repeatedly. It should call fn n times if n is an integer
# and up to n seconds if n is a floating point number.

def timecalls(n, fn, *args):
    """
    Call fn(*args) repeatedly:
    n times if n is an int, or up to
    n seconds if n is a float;
    return the min, avg, and max time
    """
    # Your code here.
    if isinstance(n, int):
        times = [timecall(fn, *args)[0] for _ in range(n)]
    else:
        times = []
        while sum(times) < n:
            times.append(timecall(fn, *args)[0])
    return min(times), average(times), max(times)

def average(numbers):
    return sum(numbers) / float(len(numbers))

print 'ZebraPuzzle (min, ave, max) time over 10 runs = (%gs, %gs, %gs)' % timecalls(10, zebra_puzzle)


"""
===========================================================================
1. generator function
"""
# ------------
# User Instructions
#
# Define a function, all_ints(), that generates the
# integers in the order 0, +1, -1, +2, -2, ...

def ints(start, end = None):
    i = start
    while i <= end or end is None:
        yield i
        i = i + 1


def all_ints():
    "Generate integers in the order 0, +1, -1, +2, -2, +3, -3, ..."
    yield 0
    for i in ints(1):
        yield i
        yield -i

g = all_ints()
for i in range(10):
    print next(g)