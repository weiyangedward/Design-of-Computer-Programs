from __future__ import division # use integer division rules in python3 3/2 = 1.5
from Tools import *

"""
===========================================================================
1. solve(formula) -> solve equation by filling in digits
2. fill_in(formula) -> Generate all possible fillings-in of letters
    in formula with digits
"""
# -------------
# User Instructions
#
# Write a function, solve(formula) that solves cryptarithmetic puzzles.
# The input should be a formula like 'ODD + ODD == EVEN', and the
# output should be a string with the digits filled in, or None if the
# problem is not solvable.
#
# Note that you will not be able to run your code yet since the
# program is incomplete. Please SUBMIT to see if you are correct.

import string, re, itertools

def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    return next(f for f in fill_in(formula) if valid(f))

# assume: def fill_in(formula):
#        "Generate all possible fillings-in of letters in formula with digits."

def valid(f):
    """Formula f is valid if and only if it has no
    numbers with leading zero, and evals true."""
    try:
        return not re.search(r'\b0[0-9]', f) and eval(f) is True # not allow leading zeros and eval has to be true
    except ArithmeticError: # divide by zero
        return False

# -------------
# User Instructions
#
# Complete the fill_in(formula) function by adding your code to
# the two places marked with ?????.

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."

    letters = ''.join(set(l for l in list(formula) if l in LETTERS))
    for digits in itertools.permutations('1234567890', len(letters)):
        table = string.maketrans(letters, ''.join(digits))
        yield formula.translate(table)


f1 = "ODD + ODD == EVEN"
print solve(f1)

"""
===========================================================================
1. test cases for solve(f)
2. test() to track run time for each test case
"""

examples = """TWO + TWO == FOUR
A**2 + B**2 == C**2
X / X == X
A**N + B**N == C**N and N > 1
ATOM**0.5 == A + TO + M
GLITTERS is not GOLD
A**2 + BE**2 == BY**2""".splitlines()

def test(fn):
    print '----', fn.__name__, '----'
    t0 = time.clock()
    for example in examples:
        print
        print 13*' ', example
        print '%6.4f sec:   %s ' % timecall(fn, example)
    print '%6.4f total.' % (time.clock() - t0)

test(solve)

"""
===========================================================================
1. to make program more efficient with fewer eval() calls,
    use lambda to replace eval()
"""

f = lambda Y, O, U, M, E: (1*U+10*O+100*Y) == (1*E+10*M)**2 # YOU == ME**2
assert f(2,8,9,1,7) == eval('289 == 17**2')

"""
===========================================================================
1. compile_word(word) -> return a decimal integer expression of a word
    if non-letter str, return str
2. compile_formula(formula)
3. faster_solver(formula)
"""

# --------------
# User Instructions
#
# Write a function, compile_word(word), that compiles a word
# of UPPERCASE letters as numeric digits. For example:
# compile_word('YOU') => '(1*U + 10*O +100*Y)'
# Non-uppercase words should remain unchaged.
from math import *

def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    if not word.isupper(): return word
    res = [('%s*%s' % (10**i,L)) for i,L in enumerate(word[::-1])]
    return '(' + '+'.join(res) + ')'

word = 'YOU'
assert compile_word(word) == '(1*U+10*O+100*Y)'


def compile_formula(formula, verbose=False):
    """
    compile formula into a function.
    return letters found as a str,
    in the same order as parms of function.
    e.g. 'YOU == ME**2' -> (lambda Y, M, E, U, O: (U+10*0+100*Y) == (E+10*M)**2), 'YMEUO'
    :param formula:
    :param verbose:
    :return:
    """
    letters = ''.join(set(re.findall('[A-Z]', formula))) # set of unique letters
    parms = ', '.join(letters)
    firstletters = set(re.findall(r'\b([A-Z])[A-Z]', formula))
    tokens = map(compile_word, re.split('([A-Z]+)', formula)) # replace word to expression, '([A-Z]+)' means to split
    #  by words and keep results. e.g. 'YOU == ME**2' => ['YOU','==','ME','**2']
    body = ''.join(tokens)
    if firstletters:
        tests = ' and '.join(L+'!=0' for L in firstletters) # all >= 2 digit number's first letter cannot be zero
        body = '%s and %s' % (tests, body)
    f = 'lambda %s: (%s)' % (parms, body) # fn as eval
    if verbose: print f
    return eval(f), letters # eval() builds parsing tree and load parameters for lambda fn once


def faster_solver(formula):
    """
    given a formula 'YOU == ME**2', fill in digits to solve it.
    This version precompiles the formula: only one eval per formula
    :param formula:
    :return:
    """
    f, letters = compile_formula(formula, True)
    for digits in itertools.permutations((1,2,3,4,5,6,7,8,9,0), len(letters)):
        try:
            if f(*digits) is True:
                table = string.maketrans(letters, ''.join(map(str, digits)))
                return formula.translate(table)
        except ArithmeticError:
            pass


test(faster_solver)