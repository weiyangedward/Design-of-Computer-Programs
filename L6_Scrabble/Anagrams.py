# -----------------
# User Instructions
#
# This homework deals with anagrams. An anagram is a rearrangement
# of the letters in a word to form one or more new words.
#
# Your job is to write a function anagrams(), which takes as input
# a phrase and an optional argument, shortest, which is an integer
# that specifies the shortest acceptable word. Your function should
# return a set of all the possible combinations of anagrams.
#
# Your function should not return every permutation of a multi word
# anagram: only the permutation where the words are in alphabetical
# order. For example, for the input string 'ANAGRAMS' the set that
# your function returns should include 'AN ARM SAG', but should NOT
# include 'ARM SAG AN', or 'SAG AN ARM', etc...

import time
from collections import Counter

def is_anagram_prefix(phrase, word, Lcount):
    """
    return True if word is prefix of phrase in terms of letter counts
    Lcount is a cache of phrase
    """
    if Lcount == None:
        Lcount = dict(Counter(list(phrase.replace(' ',''))))
    Wcount = dict(Counter(list(word.replace(' ',''))))
    for w,c in Wcount.iteritems():
        if w not in Lcount or c > Lcount[w]: return False
    return True


def is_anagram(phrase, word, Lstr):
    """
    return True if phrase and word are anagrams
    Lstr is a cache of phrase
    """
    if Lstr == None:
        Lstr = ''.join(sorted(list(phrase.replace(' ',''))))
    Wstr = ''.join(sorted(list(word.replace(' ',''))))
    return Lstr == Wstr

def my_anagrams(phrase, shortest=2):
    """Return a set of phrases with words from WORDS that form anagram
    of phrase. Spaces can be anywhere in phrase or anagram. All words
    have length >= shortest. Phrases in answer must have words in
    lexicographic order (not all permutations)."""
    Lcount, Lstr = None,None
    possible_words = find_words(phrase)
    candidates = list([w] for w in possible_words)
    visited, all_anagrams = set(), set()
    while candidates:
        c = candidates.pop(0)
        c_words = ' '.join(sorted(c))
        if is_anagram(phrase, c_words, Lstr):
            all_anagrams.add(c_words)
        elif len(c_words.replace(' ','')) < len(phrase) and is_anagram_prefix(phrase, c_words.replace(' ',''), Lcount):
            for w in possible_words:
                if len(w) >= shortest and w not in c:
                    newc = c + [w]
                    newc_words = ' '.join(sorted(newc))
                    if len(newc_words.replace(' ','')) <= len(phrase) and newc_words not in visited:
                        candidates.append(newc)
                        visited.add(newc_words) # avoid dups from permutation of the same anagram: 'AN ARM SAG' and 'SAG AN ARM' ...
    return all_anagrams


def anagrams(phrase, shortest=2):
    """
    This is 80 times faster than my_anagrams
    """
    return find_anagrams(phrase.replace(' ',''),'',shortest)

def find_anagrams(letters, pre, shortest):
    results = set()
    for w in find_words(letters):
        if len(w) >= shortest and w > pre: # w > pre ensures alphabetic order
            remainder = removed(letters, w)
            if remainder:
                for rest in find_anagrams(remainder, w, shortest):
                    results.add(w + ' ' + rest) # add w to words returned from recursion
            else: # done with finding anagram
                results.add(w)
    return results



# ------------
# Helpful functions
#
# You may find the following functions useful. These functions
# are identical to those we defined in lecture.

def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

def find_words(letters):
    return extend_prefix('', letters, set())

def extend_prefix(pre, letters, results):
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            extend_prefix(pre+L, letters.replace(L, '', 1), results)
    return results

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]

def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

# ------------
# Testing
#
# Run the function test() to see if your function behaves as expected.

def test():
    t0 = time.clock()
    assert 'DOCTOR WHO' in anagrams('TORCHWOOD')
    assert 'BOOK SEC TRY' in anagrams('OCTOBER SKY')
    assert 'SEE THEY' in anagrams('THE EYES')
    assert 'LIVES' in anagrams('ELVIS')
    assert anagrams('PYTHONIC') == set([
        'NTH PIC YO', 'NTH OY PIC', 'ON PIC THY', 'NO PIC THY', 'COY IN PHT',
        'ICY NO PHT', 'ICY ON PHT', 'ICY NTH OP', 'COP IN THY', 'HYP ON TIC',
        'CON PI THY', 'HYP NO TIC', 'COY NTH PI', 'CON HYP IT', 'COT HYP IN',
        'CON HYP TI'])
    t1 = time.clock()
    print 'total time = ', (t1-t0)
    return 'tests pass'

print test()

