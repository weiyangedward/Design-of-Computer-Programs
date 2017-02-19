from functools import update_wrapper
import time

def decorator(d):
    """
    decorate decorators: copy old fn name to new fn
    """
    def _d(f):
        return update_wrapper(d(f), f)  # copy f's name to d(f), this equivalents to d(f) = update_wrapper(d(f), f)
    update_wrapper(_d, d)               # copy d's name to _d
    return _d


@decorator
def memo(f):
    """
    remember and fetch func results given args
    """
    cache = {}      # init cache for f
    def _f(*args):
        try:
            return cache[args]   # return from cache
        except KeyError:
            cache[args] = result = f(*args) # compute result and cache it
            return result
        except TypeError:       # some element is not hashable: list
            return f(args)
    return _f


@decorator
def countcalls(f):
    """
    count number of func f calls
    """
    def _f(*args):
        callcounts[_f] += 1 # increment the number of fn calls
        return f(*args)     # run fn
    callcounts[_f] = 0      # init count = 0
    return _f

countcalls = {}     # init dict for countcalls()


@decorator
def trace(f):
    """
    trace recursion calls
    """
    indent = '   '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level*indent, signature)
        trace.level += 1
        try:
            result = f(*args)
            print '%s<-- %s == %s' % ((trace.level-1)*indent, signature, result)
        finally:
            trace.level -= 1
        return result

    trace.level = 0
    return _f


@decorator
def disable(f):
    """
    disable decorator
    """
    return f

@decorator
def timecall(f):
    def _f(*args):
        t0 = time.clock()
        res = f(*args)
        t1 = time.clock()
        print '%s\ttime = %gs' % (f.__name__, (t1-t0))
        return res
    return _f
