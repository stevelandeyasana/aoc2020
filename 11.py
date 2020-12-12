#!/usr/bin/env python

from util import *

grid = Grid(lines=read_data())

# print(grid)

def process_cell(g1, g2, coord):
    deltas = [
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]
    empties = 0
    occs = 0
    seat = g1[coord]
    for delta in deltas:
        telescope = 1
        char = g1.neighbor(coord, delta)
        while char is not None:
            if char == 'L':
                empties += 1
                break
            elif char == '#':
                occs += 1
                break
            telescope += 1
            char = g1.neighbor(coord, (delta[0] * telescope, delta[1] * telescope))
    if seat == 'L' and occs == 0:
        g2[coord] = '#'
    elif seat == '#' and occs >= 5:
        g2[coord] = 'L'
    return

def iter(g):
    next_g = g.copy()
    for coord in g.coords:
        process_cell(g, next_g, coord)
    return next_g

last_g = grid
next_g = iter(grid)
next_g.print()
while last_g != next_g:
    last_g = next_g
    next_g = iter(last_g)
next_g.print()

count = sum(1 for coord in next_g.coords if next_g[coord] == '#')

answer = count
print(answer)
sys.exit(0)
from aocd import submit
submit(answer, part="b", day=11, year=2020)
