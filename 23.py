#!/usr/bin/env python

from util import *

PART = "a"

CUPS = [int(c) for c in list(read_data())[0] if c in '1234567890']

def iter_cups(cups):
    min_cup = min(*cups)
    max_cup = max(*cups)
    # print(cups)
    # print('curr:', cups[0])
    current = cups[0]
    picked_up = cups[1:4]
    remaining = cups[4:]
    dest_cup = current - 1
    if dest_cup < min_cup:
        dest_cup = max_cup
    # print(picked_up, dest_cup)
    while dest_cup not in remaining:
        # print('look for', dest_cup, 'in', remaining)
        dest_cup -= 1
        if dest_cup < min_cup:
            dest_cup = max_cup
    # print('dest:', dest_cup)
    dest_cup_ix = remaining.index(dest_cup)
    # print('  at', dest_cup_ix)

    remaining[dest_cup_ix+1:dest_cup_ix+1] = picked_up
    # print(remaining, current)

    return remaining + [current]

    # if dest_cup_ix == 0:
    #     return [remaining[dest_cup_ix]] + picked_up + remaining[dest_cup_ix+1:] + [current]
    # elif dest_cup_ix < len(remaining) - 1:
    # result = [remaining[dest_cup_ix]] + picked_up + remaining[dest_cup_ix+1:] + remaining[0:dest_cup_ix] + [current]
    # print([remaining[dest_cup_ix]], picked_up, remaining[dest_cup_ix+1:], remaining[0:dest_cup_ix], [current])
    # result = [remaining[dest_cup_ix]] + picked_up + remaining[dest_cup_ix+1:] + remaining[0:dest_cup_ix] + [current]
    # print("=>", result)
    # return result
    # else:
    #     return [remaining[dest_cup_ix]] + picked_up + remaining[0:dest_cup_ix] + [current]

def go(cups, n_max=100, is_a=True):
    for n in range(0, n_max):
        if n % 100000 == 0:
            print(n)
        # print('----\nmove', n+1)
        cups = iter_cups(cups)
    one_ix = cups.index(1)
    result_cups = cups[one_ix+1:] + cups[0:one_ix]
    # print("final:", result_cups)
    # print(''.join([str(i) for i in result_cups]))
    if is_a:
        return ''.join([str(i) for i in result_cups])
    else:
        return result_cups[0] * result_cups[1]

def run(path):
    return go([int(c) for c in list(read_data(path=path))[0] if c in '1234567890'])

# assert iter_cups([3, 8, 9, 1, 2, 5, 4, 6, 7]) == [2,8,9,1,5,4,6,7,3]
# assert iter_cups([2,8,9,1,5,4,6,7,3]) == [5,4,6,7,8,9,1,3,2]
# assert iter_cups([5,4,6,7,8,9,1,3,2]) == [8,9,1,3,4,6,7,2,5]
# print(repr(go([3,8,9,1,2,5,4,6,7])))
# assert go([3,8,9,1,2,5,4,6,7]) == '67384529'

# answer = run('23.txt')

MILL_CUPS = [] + CUPS
next_cup = max(*CUPS) + 1
print("priming da cups")
while len(MILL_CUPS) < 1_000_000:
    MILL_CUPS.append(next_cup)
    next_cup += 1

answer = go(MILL_CUPS, n_max=10_000_000, is_a=False)

assert isinstance(answer, int)
assert answer != None
assert answer != 0
assert answer != ''

PART = "b"

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=23, year=2020)
