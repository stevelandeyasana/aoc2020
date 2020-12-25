#!/usr/bin/env python

from util import *

PART = "a"

def _read_line(line):
    i = 0
    while i < len(line):
        if line[i] in ('e', 'w'):
            yield line[i]
            i += 1
        elif line[i] in ('n', 's'):
            yield line[i] + line[i+1]
            i += 2
        else:
            assert False

def read_line(line):
    return list(_read_line(line.strip()))

NEIGHBORS_EVEN = {
    'w': V(-1, 0),
    'e': V(1, 0),
    'nw': V(-1, -1),
    'ne': V(0, -1),
    'sw': V(-1, 1),
    'se': V(0, 1),
}

NEIGHBORS_ODD = {
    'w': V(-1, 0),
    'e': V(1, 0),
    'nw': V(0, -1),
    'ne': V(1, -1),
    'sw': V(0, 1),
    'se': V(1, 1),
}

def get_neighbors(pos):
    if pos.y % 2 == 0:
        return [pos + neighbor for neighbor in NEIGHBORS_EVEN.values()]
    else:
        return [pos + neighbor for neighbor in NEIGHBORS_ODD.values()]

def get_pos(line):
    pos = V(0, 0)
    for move in line:
        if pos.y % 2 == 0:
            pos += NEIGHBORS_EVEN[move]
        else:
            pos += NEIGHBORS_ODD[move]
    return pos


def run(path):
    print('run', path)
    blacks = set()
    for line in read_data(path):
        print(read_line(line))
        pos = get_pos(read_line(line))
        if pos in blacks:
            blacks.remove(pos)
        else:
            blacks.add(pos)

    result = len(blacks)
    print("=>", result)
    return result

assert run('24ex.txt') == 10

# answer = run('24.txt')

PART = "b"

def run2(path):
    print('run2', path)
    blacks = set()
    for line in read_data(path):
        # print(read_line(line))
        pos = get_pos(read_line(line))
        if pos in blacks:
            blacks.remove(pos)
        else:
            blacks.add(pos)

    def black_neighbors_count(point):
        return len([p for p in get_neighbors(point) if p in blacks])

    # def white_neighbors_count(point):
    #     return len([p for p in get_neighbors(point) if p not in blacks])

    for i in range(0, 100):
        next_blacks = set(blacks)    

        white_candidates = set()
        for point in blacks:
            white_candidates |= set(get_neighbors(point))
            bnc = black_neighbors_count(point)
            if bnc == 0 or bnc > 2:
                next_blacks.remove(point)

        for point in white_candidates:
            bnc = black_neighbors_count(point)
            if bnc == 2:
                next_blacks.add(point)

        print("day", i+1)
        print(len(next_blacks))
        blacks = next_blacks

    result = len(blacks)
    print("=>", result)
    return result

assert run2('24ex.txt') == 2208
answer = run2('24.txt')

assert isinstance(answer, int)
assert answer != None
assert answer != 0
assert answer != ''

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=exercise_num(), year=2020)
