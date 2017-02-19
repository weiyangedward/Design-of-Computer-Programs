# -----------------
# User Instructions
#
# This problem deals with the one-player game foxes_and_hens. This
# game is played with a deck of cards in which each card is labelled
# as a hen 'H', or a fox 'F'.
#
# A player will flip over a random card. If that card is a hen, it is
# added to the yard. If it is a fox, all of the hens currently in the
# yard are removed.
#
# Before drawing a card, the player has the choice of two actions,
# 'gather' or 'wait'. If the player gathers, she collects all the hens
# in the yard and adds them to her score. The drawn card is discarded.
# If the player waits, she sees the next card.
#
# Your job is to define two functions. The first is do(action, state),
# where action is either 'gather' or 'wait' and state is a tuple of
# (score, yard, cards). This function should return a new state with
# one less card and the yard and score properly updated.
#
# The second function you define, strategy(state), should return an
# action based on the state. This strategy should average at least
# 1.5 more points than the take5 strategy.

import random
from Tools import *
from functools import update_wrapper


def foxes_and_hens(strategy, foxes=7, hens=45):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    state = (score, yard, cards) = (0, 0, 'F'*foxes + 'H'*hens)
    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard


def fh_actions(state):
    "The legal actions from a state."
    (score, yard, cards) = state
    res = []
    if yard > 0: res.append('gather')       # only allow gather when yard > 0
    if len(cards) > 0: res.append('wait')
    return res


def fh_actionScore(state, action, fh_stateScore):
    """
    The expected value of choosing action in state.
    """
    (score, yard, cards) = state
    if action == 'gather':                          # gather action will cause the next card to be lost
        return sum(fh_stateScore(gather(state, i)) for i in range(len(cards))) / float(len(cards))  # if gather,
        # consider all possible cards to be discarded
    if action == 'wait':
        return sum(fh_stateScore(wait(state, i)) for i in range(len(cards))) / float(len(cards))
    raise ValueError


@memo
def fh_stateScore(state):
    """
    The utility of a state;
    """
    (score, yard, cards) = state
    if len(cards) == 0:
        return score + yard
    else:
        return max(fh_actionScore(state, action, fh_stateScore) for action in fh_actions(state))


def best_action(state, actions, Q, U):
    "Return the optimal action for a state, given U."
    def EU(action):
        return Q(state, action, U)
    return max(actions(state), key=EU)


def strategy(state):
    return best_action(state, fh_actions, fh_actionScore, fh_stateScore)


def sol_strategy(state):
    (score, yard, cards) = state
    if 'F' not in cards:
        return 'wait'
    elif yard >= 3:
        return 'gather'
    else:
        return 'wait'


def gather(state, i):
    """
    generate new state after gather and discard card[i]
    """
    (score, yard, cards) = state
    card = cards[i]
    cards_left = cards.replace(card, '', 1)
    return (score + yard, 0, cards_left)


def wait(state, i):
    """
    generate new state after wait for card[i]
    """
    (score, yard, cards) = state
    card = cards[i]
    cards_left = cards.replace(card, '', 1)
    if card == 'H':
        return (score, yard+1, cards_left)
    elif card == 'F':
        return (score, 0, cards_left)


def do(action, state):
    "Apply action to state, returning a new state."
    # Make sure you always use up one card.
    (score, yard, cards) = state
    card = random.choice(cards)
    cards_left = cards.replace(card, '', 1)     # replace drawn card once with empty str
    if action == 'gather':
        return (score + yard, 0, cards_left)    # add yard to score, and discard one card
    elif action == 'wait':
        if card == 'H':
            return (score, yard+1, cards_left)
        elif card == 'F':
            return (score, 0, cards_left)
    else:
        raise ValueError


def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'


def average_score(strategy, N=1000):
    return sum(foxes_and_hens(strategy) for _ in range(N)) / float(N)


def superior(A, B=take5):
    "Does strategy A have a higher average score than B, by more than 1.5 point?"
    res = average_score(A) - average_score(B)
    print res
    return res > 1.5


def test():
    gather = do('gather', (4, 5, 'F'*4 + 'H'*10))
    assert (gather == (9, 0, 'F'*3 + 'H'*10) or
            gather == (9, 0, 'F'*4 + 'H'*9))

    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or
            wait == (10, 0, 'FHH'))

    assert superior(strategy)
    return 'tests pass'

print timecall(test)


