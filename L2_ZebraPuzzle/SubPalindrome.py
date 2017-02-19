# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes
# a string as input and returns the i and j indices that
# correspond to the beginning and end indices of the longest
# palindrome in the string.
#
# Grading Notes:
#
# You will only be marked correct if your function runs
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    if text == '': return (0,0)
    text, n = text.upper(), len(text)
    max_i, max_j, max_len = 0, 0, 1
    for i in range(n):
        max_i, max_j, max_len = find_pal(max_i, max_j, max_len, i-1, i, n, text) # even
        max_i, max_j, max_len = find_pal(max_i, max_j, max_len, i-1, i+1, n, text) # odd
    return (max_i, max_j+1)

def find_pal(max_i, max_j, max_len, s, e, n, text):
    while s >= 0 and e < n and text[s] == text[e]:
        if e-s > max_j-max_i:
            max_i, max_j, max_len = s, e, e-s
        s-=1; e+=1
    return max_i, max_j, max_len


def longest_subpalindrome_slice_slow(text):
    max_palin, max_i, max_j = '', 0, 0
    n = len(text)
    for i in range(n+1):
        for j in range(i+1,n+1):
            if is_palin(text[i:j]) and j-i > max_j-max_i:
                max_palin, max_i, max_j = text[i:j], i, j
    return (max_i, max_j)

def is_palin(s):
    s = s.upper()
    i, j = 0, len(s)-1
    while i < j:
        if s[i] != s[j]: return False
        i+=1
        j-=1
    return True

def test():
    L = longest_subpalindrome_slice
    # L = longest_subpalindrome_slice_slow
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print test()