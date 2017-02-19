import random

def shuffle(deck):
    """
    Knuth shuffle algorithm
    This algorithm creates a permutation of input deck

    1st pos, has n choice of cards
    2nd pos, has n-1 choice of cards
    3rd pos, has n-2 choice of cards
    and so on ...
    """
    n = len(deck)
    for i in range(n-1): # does not need to swap(n-1, n-1)
        swap(deck, i, random.randrange(i,n))

def swap(deck, i, j):
    """
    swap positions of two cards in a deck
    """
    deck[i], deck[j] = deck[j], deck[i]


def test(deck):
    deck = list(deck)
    n = 10000
    count = dict()
    for i in range(n):
        shuffle(deck)
        permut = ''.join(deck)
        count[permut] =  count[permut]+1 if permut in count else 1

    for i in count:
        print '%s %.3g %%' % (i, count[i] * 100. / n)

test('12')