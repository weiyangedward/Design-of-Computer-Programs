from Tools import *

"""
===========================================================================
1. bsuccessors(state) -> return a dict of successor state
"""
# -----------------
# User Instructions
#
# Write a function, bsuccessors(state), that takes a state as input
# and returns a dictionary of {state:action} pairs.
#
# A state is a (here, there, t) tuple, where here and there are
# frozensets of people (indicated by their times), and potentially
# the 'light,' t is a number indicating the elapsed time.
#
# An action is a tuple (person1, person2, arrow), where arrow is
# '->' for here to there or '<-' for there to here. When only one
# person crosses, person2 will be the same as person one, so the
# action (2, 2, '->') means that the person with a travel time of
# 2 crossed from here to there alone.

def bsuccessors(state):
    """Return a dict of {state:action} pairs. A state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the 'light', and t is a number indicating the elapsed time. Action is represented
    as a tuple (person1, person2, arrow), where arrow is '->' for here to there and
    '<-' for there to here."""
    here, there, t = state
    if 'light' in here:
        return dict(
            ((here - frozenset([a, b, 'light']), # remove set(a,b,'light') from here
            there | frozenset([a, b, 'light']),  # union set(a,b,'light') to there
            t + max(a,b)),                       # add max time to current t, here use ',' is same as ':' dict((a,b)) == dict(a:b)
            (a,b,'->'))
            for a in here if a is not 'light'
            for b in here if b is not 'light')
    else:                                        # 'light' in there
        return dict(
            ((here | frozenset([a, b, 'light']), # remove set(a,b,'light') from there
            there - frozenset([a, b, 'light']),
            t + max(a,b)),
            (a,b,'<-'))
            for a in there if a is not 'light'
            for b in there if b is not 'light')



def test1():

    assert bsuccessors((frozenset([1, 'light']), frozenset([]), 3)) == {
                (frozenset([]), frozenset([1, 'light']), 4): (1, 1, '->')}

    assert bsuccessors((frozenset([]), frozenset([2, 'light']), 0)) =={
                (frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}

    return 'tests pass'

# print test1()

"""
===========================================================================
1. path_states
2. path_actions
"""

# ----------------
# User Instructions
#
# Write two functions, path_states and path_actions. Each of these
# functions should take a path as input. Remember that a path is a
# list of [state, action, state, action, ... ]
#
# path_states should return a list of the states. in a path, and
# path_actions should return a list of the actions.

def path_states(path):
    "Return a list of states in this path."
    return path[0::2] # states are in even position, start at 0, +=2 each time

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2] # actions are in odd position

def test2():
    testpath = [
        (frozenset([1, 10]), frozenset(['light', 2, 5]), 5), # state 1
        (5, 2, '->'),                                        # action 1
        (frozenset([10, 5]), frozenset([1, 2, 'light']), 2), # state 2
        (2, 1, '->'),                                        # action 2
                (frozenset([1, 2, 10]), frozenset(['light', 5]), 5),
                (5, 5, '->'),
                (frozenset([1, 2]), frozenset(['light', 10, 5]), 10),
                (5, 10, '->'),
                (frozenset([1, 10, 5]), frozenset(['light', 2]), 2),
                (2, 2, '->'),
                (frozenset([2, 5]), frozenset([1, 10, 'light']), 10),
                (10, 1, '->'),
                (frozenset([1, 2, 5]), frozenset(['light', 10]), 10),
                (10, 10, '->'),
                (frozenset([1, 5]), frozenset(['light', 2, 10]), 10),
                (10, 2, '->'),
                (frozenset([2, 10]), frozenset([1, 5, 'light']), 5),
                (5, 1, '->'),
                (frozenset([2, 10, 5]), frozenset([1, 'light']), 1),
                (1, 1, '->')]

    assert path_states(testpath) == [
        (frozenset([1, 10]), frozenset(['light', 2, 5]), 5), # state 1
        (frozenset([10, 5]), frozenset([1, 2, 'light']), 2), # state 2
                (frozenset([1, 2, 10]), frozenset(['light', 5]), 5),
                (frozenset([1, 2]), frozenset(['light', 10, 5]), 10),
                (frozenset([1, 10, 5]), frozenset(['light', 2]), 2),
                (frozenset([2, 5]), frozenset([1, 10, 'light']), 10),
                (frozenset([1, 2, 5]), frozenset(['light', 10]), 10),
                (frozenset([1, 5]), frozenset(['light', 2, 10]), 10),
                (frozenset([2, 10]), frozenset([1, 5, 'light']), 5),
                (frozenset([2, 10, 5]), frozenset([1, 'light']), 1)]

    assert path_actions(testpath) == [(5, 2, '->'), # action 1
                                      (2, 1, '->'), # action 2
                                      (5, 5, '->'),
                                      (5, 10, '->'),
                                      (2, 2, '->'),
                                      (10, 1, '->'),
                                      (10, 10, '->'),
                                      (10, 2, '->'),
                                      (5, 1, '->'),
                                      (1, 1, '->')]
    return 'tests pass'

# print test2()

"""
===========================================================================
1. bridge_problem -> fix and find the shortest path
"""
# -----------------
# User Instructions
#
# Modify the bridge_problem(here) function so that it
# tests for goal later: after pulling a state off the
# frontier, not when we are about to put it on the
# frontier.

def bridge_problem(here): # here is a list of people at here: [1,2,5,10]
    here = frozenset(here) | frozenset(['light'])   # add light to here
    explored = set()                                # visited states
    frontier = [ [(here, frozenset(), 0)] ] # add init state to frontier, where there is no one at there, and time=0
    if len(here) == 1: return frontier[0]   # if no one is at here, we are done, just return init state at frontier
    while frontier:
        path = frontier.pop(0)
        here, there, t = path[-1]
        if not here:
            return path
        for (state, action) in bsuccessors(path[-1]).items(): # generate all possible successor states
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                frontier.append(path2)
                frontier.sort(key=elapsed_time) # order frontier by elapsed_time so that the 1st path come off
                # frontier is the shortest
    return []


def elapsed_time(path):
    return path[-1][2] # time is the 3rd element in the most recently state of a path


def test3():
    assert timecall(bridge_problem, frozenset((1, 2),))[-1][-1] == 2 # the [-1][-1] grabs the total elapsed time
    assert timecall(bridge_problem, frozenset((1, 2, 5, 10),))[-1][-1] == 17
    return 'tests pass'

print test3()


import doctest

class TestBridge: """
>>> elapsed_time(bridge_problem([1,2,5,10]))
17

## There are two equally good solutions
>>> S1 = [(2, 1, '->'), (1, 1, '<-'), (5, 10, '->'), (2, 2, '<-'), (2, 1, '->')]
>>> S2 = [(2, 1, '->'), (2, 2, '<-'), (5, 10, '->'), (1, 1, '<-'), (2, 1, '->')]
>>> path_actions(bridge_problem([1,2,5,10])) in (S1, S2)
True

## Try some other problems
>>> path_actions(bridge_problem([1,2,5,10,15,20]))
[(2, 1, '->'), (1, 1, '<-'), (10, 5, '->'), (2, 2, '<-'), (2, 1, '->'), (1, 1, '<-'), (15, 20, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> path_actions(bridge_problem([1,2,4,8,16,32]))
[(2, 1, '->'), (1, 1, '<-'), (8, 4, '->'), (2, 2, '<-'), (1, 2, '->'), (1, 1, '<-'), (16, 32, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> [elapsed_time(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
[0, 1, 2, 7, 15, 28]

>>> [elapsed_time(bridge_problem([1,1,2,3,5,8,13,21][:N])) for N in range(8)]
[0, 1, 1, 2, 6, 12, 19, 30]

>>> [elapsed_time(bridge_problem([1,2,99,100]))]
[107]

>>> S3 = [(2, 1, '->'), (1, 1, '<-'), (100, 99, '->'), (2, 2, '<-'), (2, 1, '->')]
>>> S4 = [(2, 1, '->'), (2, 2, '<-'), (100, 99, '->'), (1, 1, '<-'), (2, 1, '->')]
>>> path_actions(bridge_problem([1,2,99,100])) in (S3, S4)
True
"""

# print doctest.testmod()

"""
===========================================================================
1. Since there are lots of state share the same here and there, but differ
    in time, we can move the time out of state, and make program more efficient.
2. bsuccessors2 -> remove time from state
"""
# -----------------
# User Instructions
#
# write a function, bsuccessors2 that takes a state as input
# and returns a dictionary of {state:action} pairs.
#
# The new representation for a path should be a list of
# [state, (action, total time), state, ... , ], though this
# function will just return {state:action} pairs and will
# ignore total time.
#
# The previous bsuccessors function is included for your reference.

def bsuccessors2(state):
    """Return a dict of {state:action} pairs. A state is a
    (here, there) tuple, where here and there are frozensets
    of people (indicated by their travel times) and/or the light."""
    here, there = state
    if 'light' in here:
        return dict(
            ((here - frozenset([a, b, 'light']), # remove set(a,b,'light') from here
            there | frozenset([a, b, 'light'])), # union set(a,b,'light') to there
            (a,b,'->'))
            for a in here if a is not 'light'
            for b in here if b is not 'light')
    else: # 'light' in there
        return dict(
            ((here | frozenset([a, b, 'light']), # remove set(a,b,'light') from there
            there - frozenset([a, b, 'light'])),
            (a,b,'<-'))
            for a in there if a is not 'light'
            for b in there if b is not 'light')


def test4():
    here1 = frozenset([1, 'light'])
    there1 = frozenset([])

    here2 = frozenset([1, 2, 'light'])
    there2 = frozenset([3])

    assert bsuccessors2((here1, there1)) == {
            (frozenset([]), frozenset([1, 'light'])): (1, 1, '->')}
    assert bsuccessors2((here2, there2)) == {
            (frozenset([1]), frozenset(['light', 2, 3])): (2, 2, '->'),
            (frozenset([2]), frozenset([1, 3, 'light'])): (1, 1, '->'),
            (frozenset([]), frozenset([1, 2, 3, 'light'])): (2, 1, '->')}
    return 'tests pass'

# print test4()

"""
===========================================================================
1. path_cost(path) -> return the cost of a path
2. bcost(action) -> return cost of an action
"""
# -----------------
# User Instructions
#
# Write a function, path_cost, which takes a path as input
# and returns the total cost associated with that path.
# Remember that paths will obey the convention
# path = (state, (action, total_cost), state, ...)
#
# If a path is less than length 3, your function should
# return a cost of 0.

def path_cost(path):
    """The total cost of a path, which is stored in a tuple
    with the final action."""
    # path = (state, (action, total_cost), state, ... )
    if len(path) < 3:
        return 0
    else:
        action, total_cost = path[-2]
        return total_cost

def bcost(action):
    """Returns the cost (a number) of an action in the
    bridge problem."""
    # An action is an (a, b, arrow) tuple; a and b are
    # times; arrow is a string.
    a, b, arrow = action
    return max(a, b)

def test5():
    assert path_cost(('fake_state1', ((2, 5, '->'), 5), 'fake_state2')) == 5
    assert path_cost(('fs1', ((2, 1, '->'), 2), 'fs2', ((3, 4, '<-'), 6), 'fs3')) == 6
    assert bcost((4, 2, '->'),) == 4
    assert bcost((3, 10, '<-'),) == 10
    return 'tests pass'

# print test5()

"""
===========================================================================
1. bridge_problem2 -> make changes to adapt to change of state without time
"""
def bridge_problem2(here):
    if not here or (len(here) == 1 and 'light' in here): return frozenset([0])
    here = frozenset(here) | frozenset(['light'])
    explored = set()
    frontier = [ [(here, frozenset())] ]
    while frontier:
        path = frontier.pop(0)
        here1, there1 = state1 = final_state(path)
        if not here1 or (len(here1) == 1 and 'light' in here1):
            return path
        explored.add(state1) # only add state = (here, there) to visited, but not (here, there, time) because (here,
        # there) can be the same while cost keep increasing when a person keep going back-and-forth, and this will
        # costly to add to frontier and need to be processed each time
        pcost = path_cost(path)
        for (state, action) in bsuccessors2(state1).items():
            if state not in explored:
                total_cost = pcost + bcost(action)
                path2 = path + [(action, total_cost), state]
                add_to_frontier(frontier, path2)
    return Fail

def final_state(path):
    return path[-1]

def add_to_frontier(frontier, path):
    """
    1. not add a path to frontier if there is already another path
     at frontier that has the same final state, and the old path
     has a smaller cost
    2. add a path to frontier and delete the old path if either
        1) there is not such old path, or
        2) cost of the old path is larger
    3. this can make code more efficient
    """
    old = None
    for i, p in enumerate(frontier):
        if final_state(p) == final_state(path):
            old = i
            break
    if old is not None and path_cost(frontier[old]) < path_cost(path):
        return
    elif old is not None:
        del frontier[old]
    frontier.append(path)

import time

def timecall(fn, *args):
    t0 = time.clock()
    res = fn(*args)
    t1 = time.clock()
    print fn.__name__ + ' time = ',t1-t0
    return res

def test6():
    print [path_cost(bridge_problem2([1,2,4,8,16][:N])) for N in range(6)]
    print [path_cost(bridge_problem2([1,1,2,3,5,8,13,21][:N])) for N in range(8)]

def test7():
    print [elapsed_time(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
    print [elapsed_time(bridge_problem([1,1,2,3,5,8,13,21][:N])) for N in range(8)]

timecall(test6) # this is faster because it replace expensive path with cheaper one that has the same final state,
# and does not have to sort
timecall(test7)


"""
===========================================================================
1. bridge_problem3 -> generalize bridge_problem using lowest_cost_search
"""
# -----------------
# User Instructions
#
# Define a function, lowest_cost_search, that is similar to
# shortest_path_search, but also takes into account the cost
# of an action, as defined by the function action_cost(action)
#
# Since we are using this function as a generalized version
# of the bridge problem, all the code necessary to solve that
# problem is included below for your reference.
#
# This code will not run yet. Click submit to see if your code
# is correct.


def lowest_cost_search(start, successors, is_goal, action_cost):
    """Return the lowest cost path, starting from start state,
    and considering successors(state) => {state:action,...},
    that ends in a state for which is_goal(state) is true,
    where the cost of a path is the sum of action costs,
    which are given by action_cost(action)."""
    frontier = [ [start] ]
    explored = set()
    while frontier:
        path = frontier.pop(0)
        s = final_state(path)
        if is_goal(s): return path
        explored.add(s)
        pcost = path_cost(path)
        for (state, action) in successors(s).items():
            if state not in explored:
                pcost2 = pcost + action_cost(action)
                path2 = path + [(action, pcost2), state]
                add_to_frontier(frontier, path2)
    return Fail


# -----------------
# User Instructions
#
# In this problem, you will generalize the bridge problem
# by writing a function bridge_problem3, that makes a call
# to lowest_cost_search.

def bridge_problem3(here):
    """Find the fastest (least elapsed time) path to
    the goal in the bridge problem."""

    def is_goal(state):
        (here, there) = state
        return not here or here == set('light')

    # body of bridge_problem3
    start = (frozenset(here) | frozenset(['light']), frozenset())
    return lowest_cost_search(start, bsuccessors2, is_goal, bcost)


def test6():
    here = [1, 2, 5, 10]
    assert bridge_problem3(here) == [
            (frozenset([1, 2, 'light', 10, 5]), frozenset([])),
            ((2, 1, '->'), 2),
            (frozenset([10, 5]), frozenset([1, 2, 'light'])),
            ((2, 2, '<-'), 4),
            (frozenset(['light', 10, 2, 5]), frozenset([1])),
            ((5, 10, '->'), 14),
            (frozenset([2]), frozenset([1, 10, 5, 'light'])),
            ((1, 1, '<-'), 15),
            (frozenset([1, 2, 'light']), frozenset([10, 5])),
            ((2, 1, '->'), 17),
            (frozenset([]), frozenset([1, 10, 2, 5, 'light']))]
    return 'test passes'

# print test6()


# -----------------
# User Instructions
#
# In this problem you will be refactoring the bsuccessors function.
# Your new function, bsuccessors3, will take a state as an input
# and return a dict of {state:action} pairs.
#
# A state is a (here, there, light) tuple. Here and there are
# frozensets of people (each person is represented by an integer
# which corresponds to their travel time), and light is 0 if
# it is on the `here` side and 1 if it is on the `there` side.
#
# An action is a tuple of (travelers, arrow), where the arrow is
# '->' or '<-'. See the test() function below for some examples
# of what your function's input and output should look like.

def bsuccessors3(state):
    """Return a dict of {state:action} pairs.  State is (here, there, light)
    where here and there are frozen sets of people, light is 0 if the light is
    on the here side and 1 if it is on the there side.
    Action is a tuple (travelers, arrow) where arrow is '->' or '<-'"""
    here, there, light = state
    if light == 0:
        return dict(
            ((here - frozenset([a,b]), there | frozenset([a,b]), 1), ({a,b},'->'))
            for a in here
            for b in here
        )
    elif light == 1:
        return dict(
            ((here | frozenset([a,b]), there - frozenset([a,b]), 0), ({a,b},'<-'))
            for a in there
            for b in there
        )


def test():
    assert bsuccessors3((frozenset([1]), frozenset([]), 0)) == {
            (frozenset([]), frozenset([1]), 1)  :  (set([1]), '->')}

    assert bsuccessors3((frozenset([1, 2]), frozenset([]), 0)) == {
            (frozenset([1]), frozenset([2]), 1)    :  (set([2]), '->'),
            (frozenset([]), frozenset([1, 2]), 1)  :  (set([1, 2]), '->'),
            (frozenset([2]), frozenset([1]), 1)    :  (set([1]), '->')}

    assert bsuccessors3((frozenset([2, 4]), frozenset([3, 5]), 1)) == {
            (frozenset([2, 4, 5]), frozenset([3]), 0)   :  (set([5]), '<-'),
            (frozenset([2, 3, 4, 5]), frozenset([]), 0) :  (set([3, 5]), '<-'),
            (frozenset([2, 3, 4]), frozenset([5]), 0)   :  (set([3]), '<-')}
    return 'tests pass'

print test()