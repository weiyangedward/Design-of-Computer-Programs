import itertools
from fractions import Fraction


"""
===========================================================================
1. use enumeration to compute probability
2. product() -> create cartesian product of two input strings' letters
3. condP(predicate, event) -> compute conditional probability = predicate / event
"""
sex = 'BG'

def product(*variables):
    """
    create cartesian product of multiple strs
    :param variables: multiple str
    :return: list of str, each str is a cartesian product of element from each var in *variable
    """
    return map(''.join, itertools.product(*variables))

two_kids = product(sex, sex)

one_boy = [s for s in two_kids if 'B' in s]

def two_boys(s):
    return s.count('B') == 2

def condP(predicate, event):
    """
    conditional probability: P(predicate(s) | s in event)
    = proportion of states in event for which predicate is true
    :return: frac of probability
    """
    pred = [s for s in event if predicate(s)]
    return Fraction(len(pred), len(event))

print condP(two_boys, one_boy)

"""
===========================================================================
1. another application of conditional probability
2. Out of all families with two kids with at least one boy born on Tuesday,
    what is the probability of two boys?
"""

day = 'SMTWtFs'

two_kids_bday = product(sex, day, sex, day)

boy_tuesday = [s for s in two_kids_bday if 'BT' in s]

print condP(two_boys, boy_tuesday) # 13/27

"""
#(2boys | at least one boy & a Tuesday boy) = 7 + 7 - 1 (BTBT double-counted) = 13
"""