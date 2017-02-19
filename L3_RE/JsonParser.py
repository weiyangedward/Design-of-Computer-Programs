# ---------------
# User Instructions
#
# In this problem, you will be using many of the tools and techniques
# that you developed in unit 3 to write a grammar that will allow
# us to write a parser for the JSON language.
#
# You will have to visit json.org to see the JSON grammar. It is not
# presented in the correct format for our grammar function, so you
# will need to translate it.

# ---------------
# Provided functions
#
# These are all functions that were built in unit 3. They will help
# you as you write the grammar.  Add your code at line 102.

from functools import update_wrapper
from string import split
import re
from Tools import *


def split(text, sep=None, maxsplit=-1):
    """
    strip space for each element in string
    """
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]


def grammar(description, whitespace=r'\s*'):
    """
    Convert a description to a grammar.  Each line is a rule for a
    non-terminal symbol; it looks like this:

        Symbol =>  A1 A2 ... | B1 B2 ... | C1 C2 ...

    where the right-hand side is one or more alternatives, separated by
    the '|' sign.  Each alternative is a sequence of atoms, separated by
    spaces.  An atom is either a symbol on some left-hand side, or it is
    a regular expression that will be passed to re.match to match a token.

    Notation for *, +, or ? not allowed in a rule alternative (but ok
    within a token). Use '\' to continue long lines.  You must include spaces
    or tabs around '=>' and '|'. That's within the grammar description itself.
    The grammar that gets defined allows whitespace between tokens by default;
    specify '' as the second argument to grammar() to disallow this (or supply
    any regular expression to describe allowable whitespace between tokens).
    """
    G = {' ': whitespace}
    description = description.replace('\t', ' ') # no tabs!
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G


def parse(start_symbol, text, grammar): # grammer is a dict(), and so cannot be decorated by memo
    """
    Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure iff remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'
    """

    tokenizer = grammar[' '] + '(%s)' # parse [+-] with space defined in grammar

    def parse_sequence(sequence, text): # parse seq of items
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        # print atom, text
        if atom in grammar:  # Non-Terminal: tuple of alternatives, when atom is defined in grammar, e.g. 'Exp'
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree, rem
            return Fail
        else:  # Terminal: match characters against start of text, when atom is RE, e.g. [+-]
            m = re.match(tokenizer % atom, text) # insert atom to tokenizer and match against text
            return Fail if (not m) else (m.group(1), text[m.end():])

    # Body of parse:
    return parse_atom(start_symbol, text)

Fail = (None, None)


G = grammar(r"""
Exp     =>  Term [+-] Exp | Term
Term    =>  Factor [*/] Term | Factor
Factor  =>  Funcall | Var | Num | [(] Exp [)]
Funcall =>  Var [(] Exps [)]
Exps    =>  Exp [,] Exps | Exp
Var     =>  [a-zA-Z_]\w*
Num     =>  [-+]?[0-9]+([.][0-9]*)?
""", whitespace='\s*')

# print parse('Exp', 'a * x', G)

"""
write description for Json
"""
JSON = grammar("""
value => object | array | string | number | true | false | null
object => { members } | { }
members => pair , members | pair
pair => string : value
string => "[a-zA-Z\s]*"
array => [[] elements []] | [[][]]
elements => value [,] elements | value
number => int frac exp | int exp | int frac | int
int => -?[1-9][0-9]*
frac => [.][0-9]+
exp => [eE][+-]?[0-9]+
""", whitespace='\s*')


def json_parse(text):
    return parse('value', text, JSON)


def test():
    print json_parse('["testing", 1, 2, 3]')
    assert json_parse('["testing", 1, 2, 3]') == (['value',
                           ['array',
                            '[',
                            ['elements',
                                   ['value',
                                    ['string',
                                     '"testing"']
                                   ],
                                   ',',
                                   ['elements',
                                       [
                                           'value',
                                           [
                                               'number',
                                               [
                                                   'int',
                                                   '1'
                                               ]
                                           ]
                                       ],
                                       ',',
                                       [
                                           'elements',
                                           [
                                               'value',
                                               [
                                                   'number',
                                                   [
                                                       'int',
                                                       '2'
                                                   ]
                                               ]
                                           ],
                                           ',',
                                           [
                                               'elements',
                                               [
                                                   'value',
                                                   [
                                                       'number',
                                                       [
                                                           'int',
                                                           '3'
                                                       ]
                                                   ]
                                               ]
                                           ]
                                       ]
                                   ]
                               ],
                               ']'
                           ]
                       ],'')

    print '----------'
    print json_parse('-123.456e+789')
    assert json_parse('-123.456e+789') == \
           (
                       [
                           'value',
                           [
                               'number',
                               [
                                   'int',
                                   '-123'
                               ],
                               [
                                   'frac',
                                   '.456'
                               ],
                               [
                                   'exp',
                                   'e+789'
                               ]
                           ]
                       ],
                       ''
           )

    print '----------'
    print json_parse('{"age": 21, "state":"CO","occupation":"rides the rodeo"}')
    assert json_parse('{"age": 21, "state":"CO","occupation":"rides the rodeo"}') == \
           (
                      [
                          'value',
                          [
                              'object',
                              '{',
                              [
                                  'members',
                                  [
                                      'pair',
                                      [
                                          'string',
                                          '"age"'
                                      ],
                                      ':',
                                      [
                                          'value',
                                          [
                                              'number',
                                              [
                                                  'int',
                                                  '21'
                                              ]
                                          ]
                                      ]
                                  ],
                                  ',',
                                  [
                                      'members',
                                      [
                                          'pair',
                                          [
                                              'string',
                                              '"state"'
                                          ],
                                          ':',
                                          [
                                              'value',
                                              ['string',
                                               '"CO"'
                                               ]
                                          ]
                                      ],
                                      ',',
                                      [
                                          'members',
                                          [
                                              'pair',
                                              [
                                                  'string',
                                                  '"occupation"'
                                              ],
                                              ':',
                                              ['value',
                                               ['string',
                                                '"rides the rodeo"']
                                               ]
                                          ]
                                      ]
                                  ]
                              ],
                              '}']
                      ], '')
    return 'tests pass'

print test()