#!/usr/bin/env python

from util import *

PART = "a"

def parse(path):
    with open(path, 'r') as f:
        decks = f.read().split('\n\n')
        deck1 = [int(s) for s in decks[0].splitlines()[1:]]
        deck2 = [int(s) for s in decks[1].splitlines()[1:]]
        return deck1, deck2

def run(path):
    decks = parse(path)
    n = 0
    while decks[0] and decks[1]:
        n += 1
        print(decks[0])
        print(decks[1])
        a = decks[0].pop(0)
        b = decks[1].pop(0)
        print(a, 'vs', b)
        if a > b:
            print('1 win')
            decks[0].extend([a, b])
        elif a < b:
            print('2 win')
            decks[1].extend([b, a])
        # if n > 2:
        #     return
    for deck in decks:
        if deck:
            print(deck)
            result = 0
            for i, card in enumerate(reversed(deck)):
                print(card, i+1)
                result += card * (i + 1)
            print(result)
            return result


assert run('22ex.txt') == 306
answer = run('22.txt')
assert isinstance(answer, int)
assert answer != None
assert answer != 0
assert answer != ''

# PART = "b"

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=22, year=2020)
