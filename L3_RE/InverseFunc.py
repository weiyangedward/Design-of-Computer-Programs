# --------------
# User Instructions
#
# Write a function, inverse, which takes as input a monotonically
# increasing (always increasing) function that is defined on the
# non-negative numbers. The runtime of your program should be
# proportional to the LOGARITHM of the input. You may want to
# do some research into binary search and Newton's method to
# help you out.
#
# This function should return another function which computes the
# inverse of the input function.
#
# Your inverse function should also take an optional parameter,
# delta, as input so that the computed value of the inverse will
# be within delta of the true value.

# -------------
# Grading Notes
#
# Your function will be called with three test cases. The
# input numbers will be large enough that your submission
# will only terminate in the allotted time if it is
# efficient enough.

from functools import update_wrapper
import time, math
from Tools import *


def slow_inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x)-y < y-f(x-delta)) else x-delta
    return f_1

def inverse(f, delta = 1/128.):
    """
    Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta.

    does not work for power10
    """
    def f_1(y):
        x = 10.0
        while abs(f(x) - y) > delta:
            if f(x) > y:
                x = x - (f(x) - y) / (2 * x)
            else:
                x = (y - f(x)) / (2 * x) + x
        return x
    return f_1

def inverse_bs(f, delta=1/1024.):
    """
    Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta.
    """
    def f_1(y):
        lo, hi = find_bound(f, y)
        return binary_search(f, y, lo, hi, delta)
    return f_1

def find_bound(f, y):
    """
    find value lo and hi such that f(lo) <= y <= f(hi)
    """
    x = 1.
    while f(x) < y:
        x *= 2
    lo = 0 if x == 1. else x/2
    return lo, x

def binary_search(f, y, lo, hi, delta):
    """
    given f(lo) <= y <= f(hi)
    return x such that f(x) is within delta of y
    """
    while lo < hi:
        x = (lo + hi)/2
        if f(x) < y:
            lo = x + delta
        else:
            hi = x - delta
    return x



def test():

    def square(x): return x*x
    slow_sqrt = slow_inverse(square)
    sqrt = inverse_bs(square)

    def power10(x): return 10**x
    log10 = inverse_bs(power10)

    y = 1000

    print timecall(sqrt, y)
    print timecall(math.sqrt, y)

    print timecall(log10, y)
    print timecall(math.log10, y)

test()