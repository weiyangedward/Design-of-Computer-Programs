million = 1000000

def Q(state, action, U):
    """
    Quality: value of an action as average over possible output states
    """
    if action == 'hold':
        return U(state + 1*million)
    if action == 'gamble':
        return U(state + 3*million) * .5 + U(state) * .5

def actions(state):
    return ['hold', 'gamble']

def identity(x):
    """
    Utility: value of a state
    """
    return x

def best_action(state, actions, Q, U):
    def EU(action):
        return Q(state, action, U)
    return max(actions(state), key=EU)

print best_action(100, actions, Q, identity)

import math
print best_action(100, actions, Q, math.log) # people value money logrithmically, 3million is not much better than a
# million, therefore half a log(3million) < log(million)


print best_action(10*million, actions, Q, math.log) # state changes best action from 'hold' to 'gamble'


# cross point between 'hold' and 'gamble', where Q gives the same value:
print Q(1*million, 'hold', math.log10), Q(1*million, 'gamble', math.log10)