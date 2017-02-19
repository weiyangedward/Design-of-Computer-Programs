

"""
===========================================================================
1. search(pattern, text) -> true if pattern in text
2. match(pattern, text) -> true if pattern at the start of text
3. match1(p, text) -> true if pattern matches 1st char in text or pattern is '.'
4. match_star(p, pattern, text) -> true if p does not match, or p match
    1st char in text, and match_star of the rest text returns true
"""

def search_noAPI(pattern, text):
    """Return true if pattern appears anywhere in text
	   Please fill in the match(          , text) below.
	   For example, match(your_code_here, text)"""
    if pattern.startswith('^'):
        return match_noAPI(pattern[1:], text) # p[1:] exclude '^' and find the match of pattern
    else:
        return match_noAPI('.*' + pattern, text) # '.*' indicates there can be any str before pattern in text

def match_noAPI(pattern, text):
    """
    Return True if pattern appears at the start of text
    """
    if pattern == '':
        return True         # '' matches any string
    elif pattern == '$':
        return text == ''   # $ matches the end of string without any text
    elif len(pattern) > 1 and pattern[1] in '*?':
    	p, op, pat = pattern[0], pattern[1], pattern[2:]
        if op == '*':
            return match_star(p, pat, text)
        elif op == '?':
            if match1(p, text) and match_noAPI(pat, text[1:]): # try to match p once
                return True
            else:                           # p match 0 times
                return match_noAPI(pat, text)
    else:                                   # no special 1st char
        return (match1(pattern[0], text) and
                match_noAPI(pattern[1:], text[1:])) # match the 1st char, and then match the rest string

def match1(p, text):
    """
    return true if p is '.' or p matches 1st char in text
    """
    if not text: return False
    return p == '.' or p == text[0]


def match_star(p, pattern, text):
    """
    return true if p does not match text
    or p matches 1st char in text and match_star(p, pattern, text[1:]) == true
    """
    return (match_easy(pattern, text) or                            # match 0 time
            match1(p, text) and match_star(p, pattern, text[1:]))   # match 1 time and recursively call match_star

"""
===========================================================================
1. matchset(pattern, text) -> set of remainders

matchset is an interpreter

pattern: (a|b)+
language: {a,b,ab,ba,...}
interpreter: matchset(pat, text)

interpreter needs to do (op, x, y) = components(pattern) each time it is called,
which is repeated work and slow

compiler firstly compile the pattern and generate an object c: compile(pat) -> c
then each time we try to search for pattern in text, we only need to call c(text)
"""


#----------------
# User Instructions
#
# The function, matchset, takes a pattern and a text as input
# and returns a set of remainders. For example, if matchset
# were called with the pattern star(lit(a)) and the text
# 'aaab', matchset would return a set with elements
# {'aaab', 'aab', 'ab', 'b'}, since a* can consume one, two
# or all three of the a's in the text.
#
# Your job is to complete this function by filling in the
# 'dot' and 'oneof' operators to return the correct set of
# remainders.
#
# dot:   matches any character.
# oneof: matches any of the characters in the string it is
#        called with. oneof('abc') will match a or b or c.
import re

def matchset(pattern, text):
    """
    an interpreter to match pattern in text

    match pattern at start of text
    return a set of remainders of text

    e.g. lit('abc', 'abcdef') -> set('def')
    """
    op, x, y = components(pattern)
    if 'lit' == op:
        return set([text[len(x):]]) if text.startswith(x) else null # null is an empty set so that
                                                                    # min(set()) can be used no matter
                                                                    # what is returned
    elif 'seq' == op:
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif 'alt' == op:
        return matchset(x, text) | matchset(y ,text)
    elif 'dot' == op:
        return set([text[1:]]) if text else null
    elif 'oneof' == op:
        return set([text[1:]]) if any(text.startswith(c) for c in x) else null # x is a tuple
    elif 'eol' == op:
        return set(['']) if text == '' else null
    elif 'star' == op:
        return (set([text]) |
                set(t2 for t1 in matchset(x, text)
                    for t2 in matchset(pattern, t1) if t1 != text))
    else:
        raise ValueError('unknown pattern: %s' % pattern)

null = frozenset()

def components(pattern):
    "Return the op, x, and y arguments; x and y are None if missing."
    x = pattern[1] if len(pattern) > 1 else None
    y = pattern[2] if len(pattern) > 2 else None
    return pattern[0], x, y

def test1():
    assert matchset(('lit', 'abc'), 'abcdef')            == set(['def'])
    assert matchset(('seq', ('lit', 'hi '),
                     ('lit', 'there ')),
                   'hi there nice to meet you')          == set(['nice to meet you'])
    assert matchset(('alt', ('lit', 'dog'),
                    ('lit', 'cat')), 'dog and cat')      == set([' and cat'])
    assert matchset(('dot',), 'am i missing something?') == set(['m i missing something?'])
    assert matchset(('oneof', 'a'), 'aabc123')           == set(['abc123'])
    assert matchset(('eol',),'')                         == set([''])
    assert matchset(('eol',),'not end of line')          == frozenset([])
    assert matchset(('star', ('lit', 'hey')), 'heyhey!') == set(['!', 'heyhey!', 'hey!'])

    return 'tests pass'

print test1()


"""
===========================================================================
1. APIs to generate patterns for interpreter
"""
def lit_inter(string):  return ('lit', string)              # lit: 'a'
def seq_inter(x, y):    return ('seq', x, y)                # seq: 'ab'
def alt_inter(x, y):    return ('alt', x, y)                # alt: a|b
def star_inter(x):      return ('star', x)                  # star: a*
def plus_inter(x):      return seq_inter(x, star_inter(x))    # plus(x) means x+, text has to have >=1 x
def opt_inter(x):       return alt_inter(lit_inter(''), x)    # opt(x) means 0 or 1 x
def oneof_inter(chars): return ('oneof', tuple(chars))      # any('abc')
dot_inter = ('dot',)      # '.'
eol_inter = ('eol',)      # '$'

def test2():
    assert lit_inter('abc')                         == ('lit', 'abc')
    assert seq_inter(('lit', 'a'),('lit', 'b'))     == ('seq', ('lit', 'a'), ('lit', 'b'))
    assert alt_inter(('lit', 'a'),('lit', 'b'))     == ('alt', ('lit', 'a'), ('lit', 'b'))
    assert star_inter(('lit', 'a'))                 == ('star', ('lit', 'a'))
    assert plus_inter(('lit', 'c'))                 == ('seq', ('lit', 'c'),('star', ('lit', 'c')))
    assert opt_inter(('lit', 'x'))                  == ('alt', ('lit', ''), ('lit', 'x'))
    assert oneof_inter('abc')                       == ('oneof', ('a', 'b', 'c'))
    return 'tests pass'

print test2()

"""
===========================================================================
1. search(pattern, text)
2. match(pattern, text)
"""
#---------------
# User Instructions
#
# Complete the search and match functions. Match should
# match a pattern only at the start of the text. Search
# should match anywhere in the text.

def search_inter(pattern, text):
    """Match pattern anywhere in text;
    return longest earliest match or None."""
    for i in range(len(text)):
        m = match_inter(pattern, text[i:])
        if m is not None:       # '' is a true value
            return m

def match_inter(pattern, text):
    """Match pattern against start of text;
    return longest match found or None."""
    remainders = matchset(pattern, text)
    if remainders:
        shortest = min(remainders, key=len)     # find shortest remainder
        return text[:len(text)-len(shortest)]   # original text - shortest remainder = longest match

def test3():
    assert match_inter(('star', ('lit', 'a')),'aaabcd') == 'aaa'
    assert match_inter(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == None
    assert match_inter(('alt', ('lit', 'b'), ('lit', 'a')), 'ab') == 'a'
    assert search_inter(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == 'b'
    return 'tests pass'

print test3()


"""
===========================================================================
1. APIs to generate lambda functions with pattern compiled
2. match(pattern, text) that uses compiler APIs
3. search(pattern, text) is the same as before
"""
#----------------
# User Instructions
#
# Write the compiler for alt(x, y) in the same way that we
# wrote the compiler for lit(s) and seq(x, y).

'''
def matchset(pattern, text):
    op, x, y = components(pattern)
    if 'lit' == op:
        return set([text[len(x):]]) if text.startswith(x) else null
    elif 'seq' == op:
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif 'alt' == op:
        return matchset(x, text) | matchset(y, text)
'''

def lit(s): return lambda text: set([text[len(s):]]) if text.startswith(s) else null

def seq(x, y): return lambda text: set().union(*map(y, x(text))) # map applies y to each remainder from x(text) to
# generate a list of remainders

def alt(x, y): return lambda text: x(text) | y(text)

def oneof(chars):
    return lambda text: set([text[1:]]) if (text and text[0] in chars) else null

def star(x): # 'x*' can be: 1) [text]; or 2) remainder of text after matching x+
    return lambda text: set([text]) | set(t2
                                          for t1 in x(text) if t1 != text # if t1 == text, then x has 0 match
                                          for t2 in star(x)(t1))

def plus_inter(x):
    return seq(x, star(x))    # plus(x) means x+

dot = lambda t: set(t[1:]) if t else null
eol = lambda t: set(['']) if t == '' else null

null = frozenset([])

def test4():
    g = alt(lit('a'), lit('b'))
    assert g('abc') == set(['bc'])
    return 'test passes'

print test4()


# --------------
# User Instructions
#
# Fill out the function match(pattern, text), so that
# remainders is properly assigned.

def match(pattern, text):
    """Match pattern against start of text;
    return longest match found or None."""
    remainders = pattern(text) # no matchset is needed
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text)-len(shortest)]

def search(pattern, text):
    """Match pattern anywhere in text;
    return longest earliest match or None."""
    for i in range(len(text)):
        m = match(pattern, text[i:])
        if m is not None:       # '' is a true value
            return m


"""
===========================================================================
1. compiler above is for Recognizer task, which is used to find a pattern
    from a text. Another task is called Generator, which is to generate
    the entire language using input pattern.
2. APIs for generator
3. compiler optimization: move repeated work that does not depend on the
    parameter input out of lambda because lambda will be called many times.
    Only do these works on compile time.
"""

def lit_g(s):
    set_s = set([s]) # compiler optimization: only done once when compile
    return lambda Ns: set_s if len(s) in Ns else null # Ns is a set of ints

def alt_g(x, y):    return lambda Ns: x(Ns) | y(Ns)

def star_g(x):
    return lambda Ns: opt_g(plus_g(x))(Ns) # lit('')(Ns) | plus(x)(Ns)

def plus_g(x):      return lambda Ns: genseq(x, star_g(x), Ns, startx=1) #Tricky

def oneof_g(chars):      # return set of chars
    set_c = set(chars)
    return lambda Ns: set_c if 1 in Ns else null

def opt_g(x):       return alt_g(epsilon, x)

def seq_g(x, y):
    return lambda Ns: genseq(x, y, Ns) # seq() generates a fn. geneseq(), however, does the actual computation.

dot = oneof_g('?')
epsilon = lit_g('')   # epsilon = empty string


def genseq(x, y, Ns, startx=0): # for seq(x,y), there is no constraint for startx. however, for plus(x), set startx=1
    """
    apply all matches of seq(x,y) and x + y in Ns
    """
    if not Ns: return null
    xmatches = x(set(range(startx, max(Ns)+1))) # generate all matches of x
    Ns_x = set(len(m) for m in xmatches)        # set of ints in x matches
    Ns_y = set(n-m                              # set of ints in y matches
               for n in Ns
               for m in Ns_x
               if n-m >= 0)
    ymatches = y(Ns_y)                          # generate all matches of y
    return set(m1 + m2                          # generate matches of seq(x,y)
               for m1 in xmatches
               for m2 in ymatches
               if len(m1+m2) in Ns)

def test_gen():
    def N(x): return set(range(x+1))

    assert star_g(oneof_g('ab'))(N(2)) == set(['', 'a', 'aa', 'ab', 'ba', 'bb', 'b']) # (a|b)* = {'', 'a', 'b', 'aa',
    #  'bb', 'ab', 'ba'}, since '|' indicate any: 0, either, both

    print 'all test_gen passed!'

test_gen()

"""
===========================================================================
1. refactoring APIs
2. n_ary(f) -> replace interface of f(x,f(y,z)) by f(x,y,z) that can take
    > 2 arguments.
3. decorator notation: seq_inter_d(x,y)
4. decorator(d) -> decorate decorators and copy old fn name to new fn
"""
# ---------------
# User Instructions
#
# Write a function, n_ary(f), that takes a binary function (a function
# that takes 2 inputs) as input and returns an n_ary function.

from functools import update_wrapper

def decorator(d):
    """
    decorate decorators: copy old fn name to new fn
    """
    def _d(f):
        return update_wrapper(d(f), f)  # copy f's name to d(f), this equivalents to d(f) = update_wrapper(d(f), f)
    update_wrapper(_d, d)               # copy d's name to _d
    return _d

@decorator
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    # update_wrapper(n_ary_f, f)      # copy fn name from f to n_ary_f, however, put update_wrapper in every decorator
    # violates DRY, to fix this, we define a decorator fn, that decorates decorators
    return n_ary_f

seq_inter = n_ary(seq_inter) # use fn composition to change the interface of seq_inter

print seq_inter('a', 'b', 'c') # => ('seq', 'a', ('seq', 'b', 'c'))

@n_ary
def seq_inter_d(x, y):
    return ('seq', x, y)

print seq_inter_d('a', 'b', 'c') # => ('seq', 'a', ('seq', 'b', 'c'))
print seq_inter_d.__name__       # => seq_inter_d


"""
===========================================================================
1. memo
2. countcalls
3. trace -> see the execution of program
4. disable -> return the fn without changing anything, can be used to mute decorator
"""

@decorator
def memo(f):
    """
    remember and fetch func results given args
    """
    memo.cache = {}
    def _f(*args):
        try:
            return memo.cache[args]
        except KeyError:
            memo.cache[args] = result = f(*args)
            return result
        except TypeError: # some element is not hashable: list
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

callcounts = {} # init dict for countcalls

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


# countcalls = disable
# memo = disable
trace = disable

@countcalls
@memo
@trace
def fib(n): return 1 if n <= 1 else fib(n-1) + fib(n-2)

def test_fib():
    print '%s\t%s\t%s' % ('n', 'fib(n)', 'calls')
    for i in range(0,20):
        memo.cache.clear()      # reset cache
        callcounts[fib] = 0     # reset count
        res = fib(i)
        print '%d\t%d\t%d' % (i, res, callcounts[fib])

# test_fib()


# fib(6)


"""
===========================================================================
1. grammar() -> parse grammar of a language
2. RE gives a Recognizer, a parser gives us a tree structure of expression
"""
def grammar(description, whitespace=r'\s*'):
    """
    convert a description to a grammar
    """
    G = {' ': whitespace}
    description = description.replace('\t', ' ') # no tabs
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def split(text, sep=None, maxsplit=-1):
    """
    strip space for each element in string
    """
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]

G = grammar(r"""
Exp     => Term [+-] Exp | Term
Term     => Factor [*/] Term | Factor
Factor     => funcall | Var | Num | [(] Exp [)]
Funcall     => Var [(] Exp [)]
Exps     => Exp [,] Exps | Exp
Var     => [a-zA-Z_]\w*
Num     => [-+]?[0-9]+([.][0-9]*)?
""")


def test_grammer():
    for g in G:
        print g, G[g]

# test_grammer()


def parse(start_symbol, text, grammar):
    tokenizer = grammar[' '] + '(%s)' # look up at grammar for space ' '

    def parse_seqence(sequence, text): # sequence is a list of atoms
        result = []
        for atom in sequence:                   # atom is a symbol in grammar
            tree, text = parse_atom(atom, text) # update text each time
            if text is None: return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        if atom in grammar:
            for alternative in grammar[atom]: # for each list in tuple
                tree, rem = parse_seqence(alternative, text)
                if rem is not None: return [atom] + tree, rem
            return Fail
        else:               # atom is a RE, e.g. [+-], [*/]
            m = re.match(tokenizer % atom, text) # try to match atom in text
            return Fail if not m else (m.group(1), text[m.end():])

    # body of parse
    return parse_atom(start_symbol, text)

Fail = (None, None)

print parse('Exp', 'a * x', G) # parse an expression written in 'a * x'



