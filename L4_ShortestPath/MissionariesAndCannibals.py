"""
===========================================================================
1. csuccessors(state) -> generate all successors of current state
2. delta -> difference in number of M and C and boat state in each action
3. add(x,y) -> add two tuples
4. sub(x,y) -> subtract tuple y from tuple x
5. mc_problem -> solve the MC problem
"""
# -----------------
# User Instructions
#
# Write a function, csuccessors, that takes a state (as defined below)
# as input and returns a dictionary of {state:action} pairs.
#
# A state is a tuple with six entries: (M1, C1, B1, M2, C2, B2), where
# M1 means 'number of missionaries on the left side.'
#
# An action is one of the following ten strings:
#
# 'MM->', 'MC->', 'CC->', 'M->', 'C->', '<-MM', '<-MC', '<-M', '<-C', '<-CC'
# where 'MM->' means two missionaries travel to the right side.
#
# We should generate successor states that include more cannibals than
# missionaries, but such a state should generate no successors.

def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    M1, C1, B1, M2, C2, B2 = state
    if C1 > M1 > 0 or C2 > M2 > 0 or M1 < 0 or C1 < 0 or M2 < 0 or C2 < 0: return {} # when more cannibals than
    # missionaries,
    # or negative number of people, return empty dict
    succ = []
    if B1 == 1: succ += [(add(state, d), a + '->') for d, a in delta.items()]
    if B2 == 1: succ += [(sub(state, d), '<-' + a) for d, a in delta.items()]
    return dict(succ)

# difference between left and right group after action
delta = {( 0, -1, -1,  0,  1,  1):'C',
         (-1,  0, -1,  1,  0,  1):'M',
         (-2,  0, -1,  2,  0,  1):'MM',
         (-1, -1, -1,  1,  1,  1):'MC',
         ( 0, -2, -1,  0,  2,  1):'CC'}

# add two vectors
def add(X, Y):
    return tuple(a+b for a,b in zip(X, Y))

# subtract a vector from another
def sub(X, Y):
    return tuple(a-b for a,b in zip(X, Y))



def test1():
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->',
                                               (1, 2, 0, 1, 0, 1): 'M->',
                                               (0, 2, 0, 2, 0, 1): 'MM->',
                                               (1, 1, 0, 1, 1, 1): 'MC->',
                                               (2, 0, 0, 0, 2, 1): 'CC->'}
    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C',
                                               (2, 1, 1, 3, 3, 0): '<-M',
                                               (3, 1, 1, 2, 3, 0): '<-MM',
                                               (1, 3, 1, 4, 1, 0): '<-CC',
                                               (2, 2, 1, 3, 2, 0): '<-MC'}
    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}
    return 'tests pass'

# print test1()


def mc_problem(start=(3,2,1,0,0,0), goal=None):
    if goal is None: goal = (0,0,0) + start[:3] # define the goal

    if start == goal: return [start]
    explored = set()
    frontier = [ [start] ]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in csuccessors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if state == goal:
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []

# print mc_problem()

"""
===========================================================================
1. shortest_path_search -> generalize MC problem to path search problem
2. mc_problem2 -> redefine the MC problem using shortest path search
"""
# -----------------
# User Instructions
#
# Write a function, shortest_path_search, that generalizes the search algorithm
# that we have been using. This function should have three inputs, a start state,
# a successors function, and an is_goal function.
#
# You can use the solution to mc_problem as a template for constructing your
# shortest_path_search. You can also see the example is_goal and successors
# functions for a simple test problem below.

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start): return [start]
    explored = set()
    frontier = [ [start] ]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state): return path2
                else: frontier.append(path2)
    return Fail

# -----------------
# User Instructions
#
# Write a function, mc_problem2, that solves the missionary and cannibal
# problem by making a call to shortest_path_search. Add any code below
# and change the arguments in the return statement's call to the
# shortest_path_search function.

def mc_problem2(start=(3, 3, 1, 0, 0, 0), goal=None):
    if goal is None: goal = (0,0,0) + start[:3]
    def is_goal(s): return s == goal
    return shortest_path_search(start, csuccessors, is_goal)

def test3():
    assert mc_problem2(start=(1, 1, 1, 0, 0, 0)) == [
                             (1, 1, 1, 0, 0, 0), 'MC->',
                             (0, 0, 0, 1, 1, 1)]
    assert mc_problem2() == [(3, 3, 1, 0, 0, 0), 'CC->',
                             (3, 1, 0, 0, 2, 1), '<-C',
                             (3, 2, 1, 0, 1, 0), 'CC->',
                             (3, 0, 0, 0, 3, 1), '<-C',
                             (3, 1, 1, 0, 2, 0), 'MM->',
                             (1, 1, 0, 2, 2, 1), '<-MC',
                             (2, 2, 1, 1, 1, 0), 'MM->',
                             (0, 2, 0, 3, 1, 1), '<-C',
                             (0, 3, 1, 3, 0, 0), 'CC->',
                             (0, 1, 0, 3, 2, 1), '<-M',
                             (1, 1, 1, 2, 2, 0), 'MC->',
                             (0, 0, 0, 3, 3, 1)]
    return 'tests pass'

print test3()


"""
===========================================================================
1. lowest_cost_search -> generalize to lowest cost search problem using action_cost
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
        final_s = final_state(path)
        if is_goal(final_s): return path
        explored.add(final_s)
        pcost = path_cost(path)
        for (state, action) in successors(final_s).items():
            if state not in explored:
                pcost2 = pcost + action_cost(action)
                path2 = path + [(action, pcost2), state]
                add_to_frontier(frontier, path2)
    return Fail

def final_state(path): return path[-1]

def path_cost(path):
    "The total cost of a path (which is stored in a tuple with the final action)."
    if len(path) < 3:
        return 0
    else:
        action, total_cost = path[-2]
        return total_cost

def bcost(action):
    "Returns the cost (a number) of an action in the bridge problem."
    # An action is an (a, b, arrow) tuple; a and b are times; arrow is a string
    a, b, arrow = action
    return max(a, b)

def add_to_frontier(frontier, path):
    "Add path to frontier, replacing costlier path if there is one."
    # (This could be done more efficiently.)
    # Find if there is an old path to the final state of this path.
    old = None
    for i,p in enumerate(frontier):
        if final_state(p) == final_state(path):
            old = i
            break
    if old is not None and path_cost(frontier[old]) < path_cost(path):
        return # Old path was better; do nothing
    elif old is not None:
        del frontier[old] # Old path was worse; delete it
    ## Now add the new path and re-sort
    frontier.append(path)
    frontier.sort(key=path_cost)



# --------------
# Example problem
#
# Let's say the states in an optimization problem are given by integers.
# From a state, i, the only possible successors are i+1 and i-1. Given
# a starting integer, find the shortest path to the integer 8.
#
# This is an overly simple example of when we can use the
# shortest_path_search function. We just need to define the appropriate
# is_goal and successors functions.

def is_goal(state):
    if state == 8:
        return True
    else:
        return False

def successors(state):
    successors = {state + 1: '->',
                  state - 1: '<-'}
    return successors

def test2():
    print shortest_path_search(5, successors, is_goal)
    assert shortest_path_search(5, successors, is_goal) == [5, '->', 6, '->', 7, '->', 8]
    return 'tests pass'

# test2()




