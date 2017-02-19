import random
import itertools

"""
====================================================================
1. card_ranks(hand) -> order list of ranks
"""
# -----------
# User Instructions
#
# Modify the card_ranks() function so that cards with
# rank of ten, jack, queen, king, or ace (T, J, Q, K, A)
# are handled correctly. Do this by mapping 'T' to 10,
# 'J' to 11, etc...

def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['__23456789TJQKA'.index(r) for r,s in cards] # use str.index(rank) so that 'T' won't come after 'A'
    ranks.sort(reverse=True)
    return [5,4,3,2,1] if ranks == [14,5,4,3,2] else ranks # here fix the Aces issue when there is a straight

print card_ranks(['AC', '3D', '4S', 'KH']) #should output [14, 13, 4, 3]

"""
====================================================================
1. kind(n, ranks) -> rank of kinds with number == n
"""
# -----------
# User Instructions
#
# Define a function, kind(n, ranks).

from collections import Counter

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    rcount = dict(Counter(ranks))
    for r in ranks:
        if rcount[r] == n: return r # alternatively, use ranks.count(r) to check for count of r

# -----------
# User Instructions
#
# Define a function, two_pair(ranks).

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    p1 = kind(2, ranks)
    if p1:
        ranks_rev = list(reversed(ranks)) # search for another pair
        p2 = kind(2, ranks_rev)
        if p2 and p1 != p2: return (p1,p2)

def test3():
    "Test cases for the functions in poker program."
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "5S 5D 9H 9C 6S".split() # Two pairs
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    fhranks = card_ranks(fh)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert kind(2, fhranks) == 7
    return 'tests pass'

print test3()

"""
====================================================================
1. straight(ranks) -> True if is straight
2. flush(hand) -> True if is flush
"""
#
# Define two functions, straight(ranks) and flush(hand).
# Keep in mind that ranks will be ordered from largest
# to smallest.

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4

def flush(hand):
    "Return True if all the cards have the same suit."
    return len(set(s for r,s in hand)) == 1

def test2():
    "Test cases for the functions in poker program."
    sf = "6C 7C 8C 9C TC".split()
    fk = "9D 9H 9S 9C 7D".split()
    fh = "TD TC TH 7C 7D".split()
    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    assert flush(sf) == True
    assert flush(fk) == False
    return 'tests pass'

print test2()

"""
====================================================================
1. poker(hands) -> best hand based on hand_rank
2. allmax(iterable, key) -> all best hands
"""
# -----------
# User Instructions
#
# Modify the poker() function to return the best hand
# according to the hand_rank() function. Since we have
# not yet written hand_rank(), clicking RUN won't do
# anything, but clicking SUBMIT will let you know if you
# have gotten the problem right.
#

def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

# -----------
# User Instructions
#
# Write a function, allmax(iterable, key=None), that returns
# a list of all items equal to the max of the iterable,
# according to the function specified by key.

def allmax(iterable, key=None):
    """"
    Return a list of all items equal to the max of the iterable.
    allmax() is used to break ties when two hands have the same
    rank but different suits: '1S 2S 3S 4S 5S' and '1D 2D 3D 4D 5D'
    """
    key = key or (lambda x : x)
    max_rank = hand_rank(max(iterable, key=key))
    return [h for h in iterable if hand_rank(h) == max_rank]

"""
====================================================================
1. hand_rank(hand) -> rank of a hand
"""
# -----------
# User Instructions
#
# Modify the hand_rank function so that it returns the
# correct output for the remaining hand types, which are:
# full house, flush, straight, three of a kind, two pair,
# pair, and high card hands.
#
# Do this by completing each return statement below.
#
# You may assume the following behavior of each function:
#
# straight(ranks): returns True if the hand is a straight.
# flush(hand):     returns True if the hand is a flush.
# kind(n, ranks):  returns the first rank that the hand has
#                  exactly n of. For A hand with 4 sevens
#                  this function would return 7.
# two_pair(ranks): if there is a two pair, this function
#                  returns their corresponding ranks as a
#                  tuple. For example, a hand with 2 twos
#                  and 2 fours would cause this function
#                  to return (4, 2).
# card_ranks(hand) returns an ORDERED tuple of the ranks
#                  in a hand (where the order goes from
#                  highest to lowest rank).
#
# Since we are assuming that some functions are already
# written, this code will not RUN. Clicking SUBMIT will
# tell you if you are correct.

def hand_rank(hand):
    """
    return a tuple indicates ranking of a hand: (rank, tie breaker)
    """
    ranks = card_ranks(hand) # a sorted list of rank numbers given a hand
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                                          # high card
        return (0, ranks)



def test1():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split() # => ['6C', '7C', '8C', '9C', 'TC']
    fk = "9D 9H 9S 9C 7D".split()
    fh = "TD TC TH 7C 7D".split()
    p = '6C 6D 7C 8C 9C'.split()
    assert poker([sf, fk, fh]) == [sf]

    # Add 2 new assert statements here. The first
    # should check that when fk plays fh, fk
    # is the winner. The second should confirm that
    # fh playing against fh returns fh.
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh,fh] # extreme test

    # Add 2 new assert statements here. The first
    # should assert that when poker is called with a
    # single hand, it returns that hand. The second
    # should check for the case of 100 hands.
    assert poker([fh]) == [fh]
    assert poker([fh]*100) == [fh]*100

    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)

    assert card_ranks(sf) == [10,9,8,7,6]

    assert poker([sf, sf]) == [sf,sf]

    print hand_rank(p)

    return 'tests pass'

print test1()

"""
====================================================================
1. deal(numhands, n, deck) -> list of hands, each hand has n cards
"""
# -----------
# User Instructions
#
# Write a function, deal(numhands, n=5, deck), that
# deals numhands hands with n cards each.
#

import random # this will be a useful library for shuffling

# This builds a deck of 52 cards. If you are unfamiliar
# with this notation, check out Andy's supplemental video
# on list comprehensions (you can find the link in the
# Instructor Comments box below).

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

def deal(numhands, n=5, deck=mydeck):
    random.shuffle(deck)
    return [deck[h*n:h*n+n] for h in range(numhands)]

print deal(2,7)

"""
====================================================================
1. hand_percentages(n) -> compute statistics of cards
"""
hand_names = ['Straight Flush', '4 of a Kind', 'Full House',
              'Flush', 'Straight', '3 of a Kind', '2 pair', 'Pair', 'High Card']
hand_names = list(reversed(hand_names))

def hand_percentages(n=700*1000):
    """
    sample n random hands and print a table of percentages for each
    type of hand
    """
    counts = [0] * 9
    for i in range(n/10):
        hands = deal(10)
        for h in hands:
            r = hand_rank(h)[0]
            counts[r] += 1
    for i in reversed(range(9)):
        print '%14s: %6.3f %%' % (hand_names[i], 100.*counts[i]/n)

hand_percentages(7000)


"""
====================================================================
1. refactory hand_rank() so that it has DRY property
"""
def hand_rank_refactoring(hand):
    """
    group(7, 10, 7, 9, 7) -> (3,1,1), (7,10,9)
    """
    groups = group(["--23456789TJQKA".index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    # handle exception case
    if ranks == (14,5,4,3,2): ranks = (5,4,3,2,1)
    straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1

    return (9 if (5,) == counts else
            8 if straight and flush else
            7 if (4,1) == counts else
            6 if (3,2)== counts else
            5 if flush else
            4 if straight else
            3 if (3,1,1) == counts else
            2 if (2,2,1) == counts else
            1 if (2,1,1,1) == counts else
            0), ranks

def group(items):
    """
    return a list of pairs, where each pair = (count, rank)
    e.g. [7, 10, 7, 9, 7] -> ((3,7), (1,10), (1,9))
    """
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)


def unzip(pairs):
    """
    transpose a zip
    """
    return zip(*pairs)

