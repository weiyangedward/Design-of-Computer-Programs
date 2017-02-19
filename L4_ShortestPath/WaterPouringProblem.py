

"""
===========================================================================
1. to generalize pouring problem, we can change the successor function
2. pour_problem(X, Y, goal, start=(0,0)) -> return the path with smallest
    amount of steps
"""

def pour_problem(X, Y, goal, start=(0,0)):
    """
    (x,y) is current fill levels and represent a state
    the goal is a level reached by either jar
    start at start state and follow successors until reaching the goal
    successors are set of states reached by current state
    keep track of frontier and prevoiusly visited states
    fail when no frontier
    :param X: capacity of 1st jar
    :param Y: capacity of 2nd jar
    :param goal: target amount
    :param start: start state of two jars, (0,0) -> both jars are empty
    :return:
    """
    if goal in start: return [start] # if goal = 0, then the start state already reach the goal, and so return it
    explored = set() # visited states
    frontier = [ [start] ] # frontier states
    while frontier:
        path = frontier.pop(0) # pop the 1st path at frontier
        (x,y) = path[-1] # the current state of path
        for (state, action) in successors(x, y, X, Y).items(): # successor is a dict of possible moves
            if state not in explored: # state is not visited
                explored.add(state) # add to explored set
                path2 = path + [action, state] # create a longer path
                if goal in state: # if goal is reached, return path
                    return path2
                else: # otherwise append path to frontier
                    frontier.append(path2)
    return Fail # goal state cannot be reached

Fail = []


def successors(x, y, X, Y):
    """
    return a dict of {state:action} pairs describing what can be reached
    from (x,y) state, and how
    """
    assert x <= X and y <= Y # current state (x,y) has level less than capacity
    return {((0, y+x) if y+x<=Y else (x-(Y-y), y+(Y-y))):'X->Y',
            ((x+y,0) if x+y<=X else (x+(X-x), y-(X-x))):'X<-Y',
            (X, y):'fill X', (x, Y):'fill Y',
            (0, y):'empty X', (x, 0):'empty Y'}



import doctest


class Test: """
>>> successors(0,0,4,9)
{(0, 9): 'fill Y', (0, 0): 'empty Y', (4, 0): 'fill X'}

## there is no (0,0):'empty X' because it hashes to the same key as (0,0):'empty Y' and so was overwritten

>>> pour_problem(4,9,6)
[(0, 0), 'fill Y', (0, 9), 'X<-Y', (4, 5), 'empty X', (0, 5), 'X<-Y', (4, 1), 'empty X', (0, 1), 'X<-Y', (1, 0), 'fill Y', (1, 9), 'X<-Y', (4, 6)]

"""

# print doctest.testmod()


"""
===========================================================================
1. more_pour_problem -> allow > 2 glasses
"""
# -----------------
# User Instructions
#
# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes
# as input capacities, goal, and (optionally) start. This function should
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the
# volume of a glass.
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i),
# ('empty', i), ('pour', i, j) where i and j are indices indicating the
# glass number.

def more_pour_problem(capacities, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number."""

    def is_goal(state):
        return goal in state

    def more_pour_successor(state):
        succ, n = [], len(state)
        succ.extend([(replace(state, i, 0), ('empty', i)) for i in range(n)])
        succ.extend([(replace(state, i, capacities[i]), ('fill', i)) for i in range(n)])
        succ.extend([(pour(state, a, b), ('pour', a, b)) for a in range(n) for b in range(n) if a != b])
        return dict(succ)


    def replace(state, i, val):
        tmp = list(state)
        tmp[i] = val
        return tuple(tmp)

    def pour(state, a, b):
        copy = [x for x in state]
        if state[a]+state[b]<=capacities[b]:
            copy[a] = 0
            copy[b] = state[a]+state[b]
        else:
            copy[a] = state[a] - (capacities[b] - state[b])
            copy[b] = capacities[b]
        return tuple(copy)

    if start == None: start = tuple([0 for _ in range(len(capacities))])
    return shortest_path_search(start, more_pour_successor, is_goal)


def shortest_path_search(start, successors, is_goal):
    """
    use BFS to Find the shortest path from start state to a state
    such that is_goal(state) is true.
    """
    if is_goal(start):
        return [start]
    explored = set()
    frontier = [ [start] ]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []

def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)]
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

print test_more_pour()
