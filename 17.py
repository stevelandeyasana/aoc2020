#!/usr/bin/env python

from util import *

PART = "a"

g = Grid3(read_data())

def grid_coords(g):
    for z in range(g.min.z - 1, g.max.z + 2):
        for x in range(g.min.x - 1, g.max.x + 2):
            for y in range(g.min.y - 1, g.max.y + 2):
                yield V3(x, y, z)


def iter_life(g):
    # print("BEGIN LIFE")
    g2 = g.copy()
    # g2.print()
    for coord in grid_coords(g):
        active_neighbors = sum(1 if g[neighbor] == '#' else 0 for neighbor in coord.neighbors)
        # print("at {}, {} neighbors".format(coord, active_neighbors))
        if g[coord] == '#':
            # If a cube is active and exactly 2 or 3 of its neighbors are also
            # active, the cube remains active. Otherwise, the cube becomes inactive.
            if active_neighbors in (2, 3):
                pass
            else:
                # print("become inactive")
                g2[coord] = '.'
        else:
            # If a cube is inactive but exactly 3 of its neighbors are active,
            # the cube becomes active. Otherwise, the cube remains inactive.
            if active_neighbors == 3:
                # print("become active")
                g2[coord] = '#'
            else:
                pass
    # print("RESULT:")
    # g2.print()
    return g2


def run():
    grid = Grid3(read_data())
    iter_life(grid)
    for i in range(0, 6):
        # grid.print()
        grid = iter_life(grid)
    return sum(1 if grid[coord] == '#' else 0 for coord in grid.coords)

answer = run()

#PART = "b"

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=17, year=2020)
