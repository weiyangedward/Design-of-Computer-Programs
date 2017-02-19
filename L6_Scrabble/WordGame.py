"""
========================================================
1. generate all prefixes can be formed from word dictionary
"""
# -----------------
# User Instructions
#
# Write a function, readwordlist, that takes a filename as input and returns
# a set of all the words and a set of all the prefixes in that file, in
# uppercase. For testing, you can assume that you have access to a file
# called 'words4k.txt'

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]

def readwordlist(filename):
    """Read the words from a file and return a set of the words
    and a set of the prefixes."""
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

def test1():
    assert len(WORDS)    == 3892
    assert len(PREFIXES) == 6475
    assert 'UMIAQS' in WORDS
    assert 'MOVING' in WORDS
    assert 'UNDERSTANDIN' in PREFIXES
    assert 'ZOMB' in PREFIXES
    return 'tests pass'

# print test1()

"""
========================================================
1. find all words in dictionary can be formed from letters on hand
"""
# -----------------
# User Instructions
#
# Write a function, extend_prefix, nested in find_words,
# that checks to see if the prefix is in WORDS and
# adds that to results if it is.
#
# If not, your function should check to see if the prefix
# is in PREFIXES, and if it is should recursively add letters
# until the prefix is no longer valid.

def find_words1(letters):
    """
    find all words can be built from a hand of letters
    1. create all possible prefix from letters by adding one letter at a time
    2. if prefix in dictionary, add to results
    3. if prefix also in prefix of words in dictionary, continuously extend prefix
    :param letters: a string of letters on one hand
    :return: a list of words that can be built from this hand
    """
    results = set()

    def extend_prefix(w, letters):
        if w in WORDS: results.add(w)
        if w in PREFIXES:
            for L in letters:
                extend_prefix(w+L, letters.replace(L, '', 1))

    extend_prefix('', letters)
    return results

def find_words(letters, pre='', results=None):
    if results is None: results = set()
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            find_words(letters.replace(L, '', 1), pre+L, results)
    return results

# print find_words('ACCORDING')

"""
=======================================================
1. find all words can be formed from letters in hand and letters on board
2. a word = hand_prefix + board_letter + hand_suffix
"""

def word_plays(hand, board_letters):
    """
    Find all word plays from hand that can be made to abut with a letter on board.
    Find prefix + L + suffix; L from board_letters, rest from hand
    """
    results = set()
    for pre in find_prefixes(hand, '', set()):
        for L in board_letters:
            add_suffixes(removed(hand, pre), pre+L, results)
    return results


def find_prefixes(hand, pre='', results=None):
    "Find all prefixes (of words) that can be made from letters in hand."
    if results is None: results = set()
    if pre in PREFIXES:
        results.add(pre)
        for L in hand:
            find_prefixes(hand.replace(L, '', 1), pre+L, results)
    return results


def add_suffixes(hand, pre, results):
    """
    Return the set of words that can be formed
    by extending pre with letters in hand.
    """
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in hand:
            add_suffixes(removed(hand, L), pre+L, results)
    return results


def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

def longest_words(hand, board_letters):
    "Return all word plays, longest first."
    return sorted(word_plays(hand, board_letters), key=len, reverse=True)

# print longest_words('QIBL', 'LAFDJAH')

import time

def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

hands = {  ## Regression test: to make sure each time the results are the same
    'ABECEDR': set(['BE', 'CARE', 'BAR', 'BA', 'ACE', 'READ', 'CAR', 'DE', 'BED', 'BEE',
         'ERE', 'BAD', 'ERA', 'REC', 'DEAR', 'CAB', 'DEB', 'DEE', 'RED', 'CAD',
         'CEE', 'DAB', 'REE', 'RE', 'RACE', 'EAR', 'AB', 'AE', 'AD', 'ED', 'RAD',
         'BEAR', 'AR', 'REB', 'ER', 'ARB', 'ARC', 'ARE', 'BRA']),
    'AEINRST': set(['SIR', 'NAE', 'TIS', 'TIN', 'ANTSIER', 'TIE', 'SIN', 'TAR', 'TAS',
         'RAN', 'SIT', 'SAE', 'RIN', 'TAE', 'RAT', 'RAS', 'TAN', 'RIA', 'RISE',
         'ANESTRI', 'RATINES', 'NEAR', 'REI', 'NIT', 'NASTIER', 'SEAT', 'RATE',
         'RETAINS', 'STAINER', 'TRAIN', 'STIR', 'EN', 'STAIR', 'ENS', 'RAIN', 'ET',
         'STAIN', 'ES', 'ER', 'ANE', 'ANI', 'INS', 'ANT', 'SENT', 'TEA', 'ATE',
         'RAISE', 'RES', 'RET', 'ETA', 'NET', 'ARTS', 'SET', 'SER', 'TEN', 'RE',
         'NA', 'NE', 'SEA', 'SEN', 'EAST', 'SEI', 'SRI', 'RETSINA', 'EARN', 'SI',
         'SAT', 'ITS', 'ERS', 'AIT', 'AIS', 'AIR', 'AIN', 'ERA', 'ERN', 'STEARIN',
         'TEAR', 'RETINAS', 'TI', 'EAR', 'EAT', 'TA', 'AE', 'AI', 'IS', 'IT',
         'REST', 'AN', 'AS', 'AR', 'AT', 'IN', 'IRE', 'ARS', 'ART', 'ARE']),
    'DRAMITC': set(['DIM', 'AIT', 'MID', 'AIR', 'AIM', 'CAM', 'ACT', 'DIT', 'AID', 'MIR',
         'TIC', 'AMI', 'RAD', 'TAR', 'DAM', 'RAM', 'TAD', 'RAT', 'RIM', 'TI',
         'TAM', 'RID', 'CAD', 'RIA', 'AD', 'AI', 'AM', 'IT', 'AR', 'AT', 'ART',
         'CAT', 'ID', 'MAR', 'MA', 'MAT', 'MI', 'CAR', 'MAC', 'ARC', 'MAD', 'TA',
         'ARM']),
    'ADEINRST': set(['SIR', 'NAE', 'TIS', 'TIN', 'ANTSIER', 'DEAR', 'TIE', 'SIN', 'RAD',
         'TAR', 'TAS', 'RAN', 'SIT', 'SAE', 'SAD', 'TAD', 'RE', 'RAT', 'RAS', 'RID',
         'RIA', 'ENDS', 'RISE', 'IDEA', 'ANESTRI', 'IRE', 'RATINES', 'SEND',
         'NEAR', 'REI', 'DETRAIN', 'DINE', 'ASIDE', 'SEAT', 'RATE', 'STAND',
         'DEN', 'TRIED', 'RETAINS', 'RIDE', 'STAINER', 'TRAIN', 'STIR', 'EN',
         'END', 'STAIR', 'ED', 'ENS', 'RAIN', 'ET', 'STAIN', 'ES', 'ER', 'AND',
         'ANE', 'SAID', 'ANI', 'INS', 'ANT', 'IDEAS', 'NIT', 'TEA', 'ATE', 'RAISE',
         'READ', 'RES', 'IDS', 'RET', 'ETA', 'INSTEAD', 'NET', 'RED', 'RIN',
         'ARTS', 'SET', 'SER', 'TEN', 'TAE', 'NA', 'TED', 'NE', 'TRADE', 'SEA',
         'AIT', 'SEN', 'EAST', 'SEI', 'RAISED', 'SENT', 'ADS', 'SRI', 'NASTIER',
         'RETSINA', 'TAN', 'EARN', 'SI', 'SAT', 'ITS', 'DIN', 'ERS', 'DIE', 'DE',
         'AIS', 'AIR', 'DATE', 'AIN', 'ERA', 'SIDE', 'DIT', 'AID', 'ERN',
         'STEARIN', 'DIS', 'TEAR', 'RETINAS', 'TI', 'EAR', 'EAT', 'TA', 'AE',
         'AD', 'AI', 'IS', 'IT', 'REST', 'AN', 'AS', 'AR', 'AT', 'IN', 'ID', 'ARS',
         'ART', 'ANTIRED', 'ARE', 'TRAINED', 'RANDIEST', 'STRAINED', 'DETRAINS']),
    'ETAOIN': set(['ATE', 'NAE', 'AIT', 'EON', 'TIN', 'OAT', 'TON', 'TIE', 'NET', 'TOE',
         'ANT', 'TEN', 'TAE', 'TEA', 'AIN', 'NE', 'ONE', 'TO', 'TI', 'TAN',
         'TAO', 'EAT', 'TA', 'EN', 'AE', 'ANE', 'AI', 'INTO', 'IT', 'AN', 'AT',
         'IN', 'ET', 'ON', 'OE', 'NO', 'ANI', 'NOTE', 'ETA', 'ION', 'NA', 'NOT',
         'NIT']),
    'SHRDLU': set(['URD', 'SH', 'UH', 'US']),
    'SHROUDT': set(['DO', 'SHORT', 'TOR', 'HO', 'DOR', 'DOS', 'SOUTH', 'HOURS', 'SOD',
         'HOUR', 'SORT', 'ODS', 'ROD', 'OUD', 'HUT', 'TO', 'SOU', 'SOT', 'OUR',
         'ROT', 'OHS', 'URD', 'HOD', 'SHOT', 'DUO', 'THUS', 'THO', 'UTS', 'HOT',
         'TOD', 'DUST', 'DOT', 'OH', 'UT', 'ORT', 'OD', 'ORS', 'US', 'OR',
         'SHOUT', 'SH', 'SO', 'UH', 'RHO', 'OUT', 'OS', 'UDO', 'RUT']),
    'TOXENSI': set(['TO', 'STONE', 'ONES', 'SIT', 'SIX', 'EON', 'TIS', 'TIN', 'XI', 'TON',
         'ONE', 'TIE', 'NET', 'NEXT', 'SIN', 'TOE', 'SOX', 'SET', 'TEN', 'NO',
         'NE', 'SEX', 'ION', 'NOSE', 'TI', 'ONS', 'OSE', 'INTO', 'SEI', 'SOT',
         'EN', 'NIT', 'NIX', 'IS', 'IT', 'ENS', 'EX', 'IN', 'ET', 'ES', 'ON',
         'OES', 'OS', 'OE', 'INS', 'NOTE', 'EXIST', 'SI', 'XIS', 'SO', 'SON',
         'OX', 'NOT', 'SEN', 'ITS', 'SENT', 'NOS'])}

def test_words():
    assert removed('LETTERS', 'L') == 'ETTERS'
    assert removed('LETTERS', 'T') == 'LETERS'
    assert removed('LETTERS', 'SET') == 'LTER'
    assert removed('LETTERS', 'SETTER') == 'L'
    t, results = timedcall(map, find_words, hands)
    for ((hand, expected), got) in zip(hands.items(), results):
        assert got == expected, "For %r: got %s, expected %s (diff %s)" % (
            hand, got, expected, expected ^ got)
    return t

# print test_words()

"""
========================================================
1. score a word given points of letters
2. find top n words sorted by score
"""
# -----------------
# User Instructions
#
# Write a function, word_score, that takes as input a word, and
# returns the sum of the individual letter scores of that word.
# For testing, you can assume that you have access to a file called
# 'words4k.txt'


POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5,
              L=1, M=3, N=1, O=1, P=3, Q=10, R=1, S=1, T=1, U=1, V=4,
              W=4, X=8, Y=4, Z=10, _=0)

def word_score(word):
    "The sum of the individual letter point scores for this word."
    return sum(POINTS[L] for L in word)

# print word_score('ABC')

def topn(hand, board_letters, n=10):
    """
    Return a list of the top n words that hand can play,
    sorted by word score.
    """
    words = word_plays(hand, board_letters)
    return sorted(words, key=word_score, reverse=True)[:n] # sorted by score

# print topn('QIBL', 'LAFDJAH')


"""
========================================================
1. find all plays given a row on the board
"""

class anchor(set):
  """
  anchor class as a subset of set to hold all valid letters
  at an anchor
  """

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

ANY = anchor(LETTERS) # an anchor can be any letter

# |A.....BE.C...D.| boarder is indicated by '|'
mnx, moab = anchor('MNX'), anchor('MOAB')
a_row = ['|','A',mnx, moab, '.','.',ANY,'B','E',ANY,'C',ANY,'.',ANY,'D',ANY,'|']
a_hand = 'ABCEHKN'

# -----------------
# User Instructions
#
# The find_prefixes function takes a hand, a prefix, and a
# results list as input.
# Modify the find_prefixes function to cache previous results
# in order to improve performance.

###Modify this function. You may need to modify
# variables outside this function as well.

prev_hand, prev_results = '', set() # cache for find_prefixes

def find_prefixes(hand, pre='', results=None):
    """
    Find all prefixes (of words) that can be made from letters in hand.
    cache the prev computed hand
    if a hand is the same as prev_hand, return prev_results
    """
    global prev_hand, prev_results
    if hand == prev_hand: return prev_results # eval one hand for all rows and cols
    if results is None: results = set()
    if pre == '':
        prev_hand, prev_results = hand, results # prev_results is the same obj as results, which gets filled with prefix in recursion
    # now do the computation
    if pre in PREFIXES:
        results.add(pre)
        for L in hand:
            find_prefixes(hand.replace(L, '', 1), pre+L, results)
    return results

def row_plays(hand, row):
    """
    return a set of legal plays on a row,
    a row play is an (start, 'WORD') pair
    """
    results = set()
    """
    to each allowable prefix ends at an anchor,
    add all suffixes, add words to results
    """
    for (i, sq) in enumerate(row[1:-1], 1):
        if isinstance(row[i], anchor):
            pre, maxsize = legal_prefix(i ,row)
            if pre: # add to the letter already on board
                start = i - len(pre) # start pos of word
                add_suffixes(hand, pre, start, row, results, anchored=False)
            else: # empty on the left, try all possible prefixes
                for pre in find_prefixes(hand): # cache prefixes from find_prefixes, so that we don't need to do this for each row and col
                    if len(pre) <= maxsize:
                        start = i - len(pre)
                        add_suffixes(removed(hand, pre), pre, start, row, results, anchored=False) # remove pre from hand since letters in pre are from hand
    return results


def legal_prefix(i, row):
    """
    a legal prefix of anchor at row[i], is either
    1. string of letters already on board,
    2. or letters from hands fit into empty squares

    legal_prefix(9, a_row) = ('BE', 2)
    legal_prefix(6, a_row) = ('', 2)
    """
    s = i
    # 1. return string of letters on board
    while is_letter(row[s-1]): s -= 1
    if s < i: return ''.join(row[s:i]), i-s

    # 2. return '' and len of empty space
    while is_empty(row[s-1]) and not isinstance(row[s-1], anchor): s -= 1
    return ('', i-s)


def is_empty(sq):
    return sq == '.' or sq == '*' or isinstance(sq, anchor) # '*' is the starting location

def is_letter(sq):
    return isinstance(sq, str) and sq in LETTERS


def add_suffixes(hand, pre, start, row, results, anchored=True):
    """
    add all possible suffixes, and add (start, word) to results
    """
    i = start + len(pre) # anchor pos
    if pre in WORDS and anchored and not is_letter(row[i]):
        """
        add pre to results if:
        1. pre in dictionary
        2. at least one anchor in pre
        2. pre is end with an empty space on board
        """
        results.add((start, pre))

    if pre in PREFIXES:
        sq = row[i]
        if is_letter(sq): # the square is a letter on board
            add_suffixes(hand, pre+sq, start, row, results, anchored=True)
        elif is_empty(sq): # the square is empty space
            possibilities = sq if isinstance(sq, anchor) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes(removed(hand, L), pre+L, start, row, results, anchored=True)
    return results


def test_row():
    assert legal_prefix(2, a_row) == ('A', 1)
    assert legal_prefix(3, a_row) == ('', 0)
    assert legal_prefix(6, a_row) == ('', 2)
    assert legal_prefix(9, a_row) == ('BE', 2)
    assert legal_prefix(11, a_row) == ('C', 1)
    assert legal_prefix(13, a_row) == ('', 1)
    print 'pass all tests!'

# test_row()

# print row_plays(a_hand, a_row)

"""
========================================================
1. find all plays on a complete board
"""
def a_board():
    return map(list, ['|||||||||||||||||',
                      '|J............I.|',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])

def show(board):
    for j, row in enumerate(board):
        for i, sq in enumerate(row):
            b = BONUS[i][j]
            if b.isdigit() or b == ':' or b == ';':
                print b,
            else:
                print board[i][j],
        print

# a_board = a_board()
# show(a_board)

ACROSS, DOWN = (1, 0), (0, 1) # Directions that words can go, ACROSS: at a row, a word can go along x-axis: the i direction

def horizontal_plays(hand, board):
    """
    find all horizontal plays: (score,(i,j),word) tuples across all rows
    """
    results = set()
    for (j, row) in enumerate(board[1:-1],1):
        set_anchors(row, j, board)
        for (i, w) in row_plays(hand, row):
            score = calculate_score(board, (i,j), ACROSS, hand, w)
            results.add( (score,(i,j),w) ) # j is pos on x-axis, i is pos on y-axis
    return results

def calculate_score(board, pos, direction, hand, word):
    """
    return the total score of a play
    """
    total, crosstotal, word_mult = 0,0,1 # word_mult is bonus: TW, DW, *
    starti, startj = pos
    di, dj = direction
    other_direction = DOWN if direction == ACROSS else ACROSS
    for (n, L) in enumerate(word):
        i, j = starti+n*di, startj+n*dj # pos of current letter
        sq = board[j][i]
        b = BONUS[j][i]
        word_mult *= (1 if is_letter(sq) else
                      3 if b == TW else 2 if b in (DW,'*') else 1)
        letter_mult = (1 if is_letter(sq) else
                       3 if b == TL else 2 if b == DL else 1)
        total += POINTS[L] * letter_mult
        # there is other words on the cross word direction
        if isinstance(sq, anchor) and sq is not ANY and direction is not DOWN: # 'is not DOWN' prevents infinite recursion when cross_word_score call calculate_score
            crosstotal += cross_word_score(board, L, (i,j), other_direction)
    return crosstotal + total * word_mult

def cross_word_score(board, L, pos, direction):
    """
    return the score of a word formed on the other direction from the main word
    """
    i, j = pos
    (j2, word) = find_cross_word(board, i, j)
    return calculate_score(board, (i,j2), DOWN, L, word.replace('.',L))


def all_plays(hand, board):
    """
    All plays in both directions.
    A play is a (score, pos, dir, word) tuple,
    where pos is an (i,j) pair, and dir is ACROSS or DOWN (global variables)
    """
    hplays = horizontal_plays(hand, board)
    vplays = horizontal_plays(hand, transpose(hand))
    return (set((score,(i,j),ACROSS,w) for (score,(i,j),w) in hplays) |
            set((score,(i,j),DOWN,w) for (score,(j,i),w) in vplays))


def set_anchors(row, j, board):
    """
    Anchors are empty squares with a neighboring letter. Some are restricted
    by cross-words to be only a subset of letters.
    This fn mutates input row
    """
    for (i, sq) in enumerate(row[1:-1], 1):
        neighborlist = (N,S,E,W) = neighbors(board, i, j)
        # Anchors are squares adjacent to a letter.  Plus the '*' square.
        if sq == '*' or (is_empty(sq) and any(map(is_letter, neighborlist))):
            if is_letter(N) or is_letter(S): # if letters are on the north or south of anchor, then it is restricted
                # Find letters that fit with the cross (vertical) word
                (j2, w) = find_cross_word(board, i, j) # j2 is the start of w
                row[i] = anchor(L for L in LETTERS if w.replace('.', L) in WORDS) # letters in anchor are all letters form a word by replacing '.'
            else: # Unrestricted empty square -- any letter will fit.
                row[i] = ANY


def find_cross_word(board, i, j):
    """
    Find the vertical word that crosses board[j][i]. Return (j2, w),
    where j2 is the starting row, and w is the word
    """
    sq = board[j][i]
    w = sq if is_letter(sq) else '.'
    # go north to find start of cross word
    for j2 in range(j, 0, -1):
        sq2 = board[j2-1][i]
        if is_letter(sq2): w = sq2 + w
        else: break
    # go south to find end of cross word
    for j3 in range(j+1, len(board)):
        sq3 = board[j3][i]
        if is_letter(sq3): w = w + sq3
        else: break
    return (j2, w)


def neighbors(board, i, j):
    """Return a list of the contents of the four neighboring squares,
    in the order N,S,E,W."""
    return [board[j-1][i], board[j+1][i], board[j][i+1], board[j][i-1]]


def transpose(matrix):
    return map(list,zip(*matrix)) # zip returns one col at a time, list(col) creates a row


"""
========================================================
1. build bonus board
"""
def bonus_template(quadrant):
    """
    make a board from the upper-left quadrant
    """
    return mirror(map(mirror, quadrant.split())) # inner loop mirror left to right, then the outter loop mirror up to down

def mirror(sequence):
    return sequence + sequence[-2::-1]

SCRABBLE = bonus_template("""
|||||||||
|3..:...3
|.2...;..
|..2...:.
|:..2...:
|....2...
|.;...;..
|..:...:.
|3..:...*
""")

BONUS = SCRABBLE

DW, TW, DL, TL = '23:;'


def show(board):
    for j, row in enumerate(board):
        for i, sq in enumerate(row):
            b = BONUS[j][i]
            print (sq if (is_letter(sq) or sq == '|') else BONUS[j][i]),
        print


def make_play(play, board):
    "Put the word down on the board."
    (score, (i, j), (di, dj), word) = play
    for n, L in enumerate(word):
        board[j+n*dj][i+n*di] = L
    return board


NOPLAY = None

def best_play(hand, board):
    "Return the highest-scoring play.  Or None."
    plays = all_plays(hand, board)
    return sorted(plays)[-1] if plays else NOPLAY



def show_best(hand, board):
    print 'Current board:'
    show(board)
    play = best_play(hand, board)
    if play:
        print '\nNew word: %r scores %d' % (play[-1], play[0])
        show(make_play(play,board))
    else:
        print 'No legal play'


if __name__ == '__main__':
    for row in BONUS: print row
    show(a_board())
    show_best(a_hand, a_board())