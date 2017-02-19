from Tools import *
"""
===========================================================================
1. hold(state) -> return a new state after hold
2. roll(state) -> return a new state after roll
"""
# -----------------
# User Instructions
#
# Write the two action functions, hold and roll. Each should take a
# state as input, apply the appropriate action, and return a new
# state.
#
# States are represented as a tuple of (p, me, you, pending) where
# p:       an int, 0 or 1, indicating which player's turn it is.
# me:      an int, the player-to-move's current score
# you:     an int, the other player's current score.
# pending: an int, the number of points accumulated on current turn, not yet scored

other = {1:0, 0:1} # switch to other player


def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    (p, me, you, pending) = state
    return (other[p], you, me+pending, 0)

def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    (p, me, you, pending) = state
    if d == 1: return (other[p], you, me+1, 0)
    else: return (p, me, you, pending+d)


def test1():
    assert hold((1, 10, 20, 7))    == (0, 20, 17, 0)
    assert hold((0, 5, 15, 10))    == (1, 15, 15, 0)
    assert roll((1, 10, 20, 7), 1) == (0, 20, 11, 0)
    assert roll((0, 5, 15, 10), 5) == (0, 5, 15, 15)
    return 'tests pass'

# print test1()


"""
===========================================================================
1. clueless -> a strategy to choose moves by random
2. hold_at -> return a strategy fn to hold at a certain pending score
"""
# -----------------
# User Instructions
#
# Write a strategy function, clueless, that ignores the state and
# chooses at random from the possible moves (it should either
# return 'roll' or 'hold'). Take a look at the random library for
# helpful functions.

import random

possible_moves = ['roll', 'hold']

def clueless(state):
    "A strategy that ignores the state and chooses at random from possible moves."
    return random.choice(possible_moves)


# -----------------
# User Instructions
#
# In this problem, you will complete the code for the hold_at(x)
# function. This function returns a strategy function (note that
# hold_at is NOT the strategy function itself). The returned
# strategy should hold if and only if pending >= x or if the
# player has reached the goal.

def hold_at(x):
    """Return a strategy that holds if and only if
    pending >= x or player reaches goal."""
    def strategy(state):
        (p, me, you, pending) = state
        return 'hold' if pending >= x or (me + pending) >= goal else 'roll'
    strategy.__name__ = 'hold_at(%d)' % x
    return strategy

# goal = 50
def test2():
    assert hold_at(30)((1, 29, 15, 20)) == 'roll'
    assert hold_at(30)((1, 29, 15, 21)) == 'hold'
    assert hold_at(15)((0, 2, 30, 10))  == 'roll'
    assert hold_at(15)((0, 2, 30, 15))  == 'hold'
    return 'tests pass'

# print test2()


"""
===========================================================================
1. play_pig(A,B) -> a two players pig game
2. dierolls() -> generate a sequence of die rolls, let us to control the game
"""
def dierolls():
    "Generate die rolls."
    while True:
        yield random.randint(1, 6)

def play_pig(A, B, dierolls=dierolls()): # dependency injection: to remove randomness
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    strategy = [A, B]
    state = (0,0,0,0)
    while True:
        (p, me, you, pending) = state
        if me >= goal:                  # me win
            return strategy[p]
        elif you >= goal:               # you win
            return strategy[other[p]]
        else:
            action = strategy[p](state)
            if action == 'hold':                    # strategy says 'hold'
                state = hold(state)
            elif action == 'roll':                  # strategy says 'roll'
                state = roll(state, next(dierolls))
            else:                                   # illegal action
                return strategy[other[p]]           # to protect ourselves from bug, any return that is not ['hold',
                # 'roll'] will result the current player immediately lose the game

def test4():
    A, B = hold_at(50), clueless
    rolls = iter([6,6,6,6,6,6,6,6,2]) # <-- Your rolls here
    assert play_pig(A, B, rolls) == A
    return 'test passes'

# print test4()


"""
===========================================================================
test non-deterministic code
1. always_roll
2. always_hold
"""
def always_roll(state):
    """
    continues to roll until pig out, each turn wins 1 point
    """
    return 'roll'

def always_hold(state):
    """
    always hold even without rolling the die, each turn wins 0 point
    """
    return 'hold'

def test3():
    for _ in range(10):
        winner = play_pig(always_hold, always_roll)
        assert winner.__name__ == 'always_roll'
    return 'tests pass'

# print test3()


"""
===========================================================================
1. max_wins -> a minimax strategy fn to return the best action
2. Pwin(state) -> utility fn
3. Q_pig(state, action, Pwin) -> quality fn
4. pig_actions(state) -> return a set of legal actions
5. best_action(state, actions, Q, U) -> try all actions and return the best one
    based on Q, U and state
"""
# -----------------
# User Instructions
#
# Write the max_wins function. You can make your life easier by writing
# it in terms of one or more of the functions that we've defined!

def Q_pig(state, action, Pwin):
    """
    The expected value of choosing action in state.
    in another word, return the (min probability to win) = 1-(opponent's max probability to win)
    """
    if action == 'hold':
        return 1 - Pwin(hold(state)) # return 1 - (opponent's max probability to win when I hold when next round if
        # opponent's)
    if action == 'roll':
        return (1 - Pwin(roll(state, 1))
                + sum(Pwin(roll(state, d)) for d in (2,3,4,5,6))) / 6. # return 1 - ave((opponent's max probability to win when I pig out when next round is opponent's) + (sum of probability to win when not pig out and next round is still
        # mine))
    raise ValueError


def pig_actions(state):
    "The legal actions from a state."
    _, _, _, pending = state
    return ['roll', 'hold'] if pending else ['roll']

goal = 40


@memo
def Pwin(state):
    """
    The utility of a state;
    here just the probability that an optimal player
    whose turn it is to move can win from the current state.
    """
    # Assumes opponent also plays with optimal strategy.
    (p, me, you, pending) = state
    if me + pending >= goal: return 1
    elif you >= goal: return 0
    else: return max(Q_pig(state, action, Pwin) for action in pig_actions(state)) # return the max of min probability to win


def best_action(state, actions, Q, U):
    "Return the optimal action for a state, given U."
    def EU(action):
        return Q(state, action, U)
    return max(actions(state), key=EU)

def max_wins(state):
    "The optimal pig strategy chooses an action with the highest win probability."
    return best_action(state, pig_actions, Q_pig, Pwin)



def test5():
    assert(max_wins((1, 5, 34, 4)))   == "roll"
    assert(max_wins((1, 18, 27, 8)))  == "roll"
    assert(max_wins((0, 23, 8, 8)))   == "roll"
    assert(max_wins((0, 31, 22, 9)))  == "hold"
    assert(max_wins((1, 11, 13, 21))) == "roll"
    assert(max_wins((1, 33, 16, 6)))  == "roll"
    assert(max_wins((1, 12, 17, 27))) == "roll"
    assert(max_wins((1, 9, 32, 5)))   == "roll"
    assert(max_wins((0, 28, 27, 5)))  == "roll"
    assert(max_wins((1, 7, 26, 34)))  == "hold"
    assert(max_wins((1, 20, 29, 17))) == "roll"
    assert(max_wins((0, 34, 23, 7)))  == "hold"
    assert(max_wins((0, 30, 23, 11))) == "hold"
    assert(max_wins((0, 22, 36, 6)))  == "roll"
    assert(max_wins((0, 21, 38, 12))) == "roll"
    assert(max_wins((0, 1, 13, 21)))  == "roll"
    assert(max_wins((0, 11, 25, 14))) == "roll"
    assert(max_wins((0, 22, 4, 7)))   == "roll"
    assert(max_wins((1, 28, 3, 2)))   == "roll"
    assert(max_wins((0, 11, 0, 24)))  == "roll"
    return 'tests pass'

# print test5()


strategies = [clueless, hold_at(goal/4), hold_at(1+goal/3), hold_at(goal/2), hold_at(goal), max_wins]

def play_tournament(strategies, rounds=100):
    """
    statistics of won games using different strategies
    each pair of strategies play 100 games
    """
    n = len(strategies)
    scores = [[0 for _ in range(n)] for _ in range(n)]

    for a in range(n):
        for b in range(n):
            if a != b:
                for i in range(rounds):
                    if play_pig(strategies[a], strategies[b]) == strategies[a]:
                        scores[a][b] += 1
                    else:
                        scores[b][a] += 1

    for row in scores:
        print row, sum(row)

# play_tournament(strategies)

"""
===========================================================================
1. win_diff -> a utility fn that changes the goal from winning to win big,
    notice that both players are assume to want to win big. So both of them
    are willing to roll when pending is small, but to hold when pending is
    big to cut down the difference at score.
"""
@memo
def win_diff(state):
    """
    maximize the difference of scores between winner and loser

    although this fn does not return a probability like Pwin() does,
    it return a max score, and so Q_pig() returns a 1-score (this can be negative),
    from which best_action() will choose the max one.
    """
    (p, me, you, pending) = state
    if me + pending >= goal or you >= goal:
        return me + pending - you
    else:
        return max(Q_pig(state, action, win_diff) for action in pig_actions(state))

def max_diffs(state):
    """A strategy that maximizes the expected difference between my final score
    and my opponent's."""
    return best_action(state, pig_actions, Q_pig, win_diff)

def test6():
    # The first three test cases are examples where max_wins and
    # max_diffs return the same action.
    assert(max_diffs((1, 26, 21, 15))) == "hold"
    assert(max_diffs((1, 23, 36, 7)))  == "roll"
    assert(max_diffs((0, 29, 4, 3)))   == "roll"
    # The remaining test cases are examples where max_wins and
    # max_diffs return different actions.
    assert(max_diffs((0, 36, 32, 5)))  == "roll"
    assert(max_diffs((1, 37, 16, 3)))  == "roll"
    assert(max_diffs((1, 33, 39, 7)))  == "roll"
    assert(max_diffs((0, 7, 9, 18)))   == "hold"
    assert(max_diffs((1, 0, 35, 35)))  == "hold"
    assert(max_diffs((0, 36, 7, 4)))   == "roll"
    assert(max_diffs((1, 5, 12, 21)))  == "hold"
    assert(max_diffs((0, 3, 13, 27)))  == "hold"
    assert(max_diffs((0, 0, 39, 37)))  == "hold"
    return 'tests pass'

# print test6()

# -----------------
# User Instructions
#
# In this problem, you will use a faster version of Pwin, which we will call
# Pwin2, that takes a state as input but ignores whether it is player 1 or
# player 2 who starts. This will reduce the number of computations to about
# half. You will define a function, Pwin3, which will be called by Pwin2.
#
# Pwin3 will only take me, you, and pending as input and will return the
# probability of winning.
#
# Keep in mind that the probability that I win from a position is always
# (1 - probability that my opponent wins).


def Pwin2(state):
   """The utility of a state; here just the probability that an optimal player
   whose turn it is to move can win from the current state."""
   _, me, you, pending = state
   return Pwin3(me, you, pending)

@memo
def Pwin3(me, you, pending):
    """
    Unlike Pwin, Pwin3 does not need to call fn Q_pig or pig_actions,
    instead, it
    :return:
    """
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else: # probability to win if action is needed
        Proll = (1 - Pwin3(you, me+1, 0) + sum(Pwin3(me, you, pending+d) for d in (2,3,4,5,6))) / 6. # probability to
        #  win when 'roll'
        return Proll if not pending else max(Proll, 1-Pwin3(you, me+pending, 0)) # max probability to win when 'hold' or
        # 'roll' when pending = 0


def test7():
    epsilon = 0.0001 # used to make sure that floating point errors don't cause test() to fail
    assert goal == 40
    assert len(Pwin3.cache) <= 50000
    assert Pwin2((0, 42, 25, 0)) == 1
    assert Pwin2((1, 12, 43, 0)) == 0
    assert Pwin2((0, 34, 42, 1)) == 0
    assert abs(Pwin2((0, 25, 32, 8)) - 0.736357188272) <= epsilon
    assert abs(Pwin2((0, 19, 35, 4)) - 0.493173612834) <= epsilon
    return 'tests pass'

# print test7()


def test8():
    print timecall(Pwin2, (0,0,0,0)) # run time is only takes half the time as in Pwin
    print len(Pwin3.cache) # size of the cache is also half
    print timecall(Pwin, (0,0,0,0))
    print len(Pwin.cache)

# test8()

goal = 60 # after increasing the speed, we can set a larger goal
print timecall(Pwin2, (0,0,0,0))
print timecall(Pwin, (0,0,0,0))

