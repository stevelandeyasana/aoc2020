#!/usr/bin/env python

from util import *

Inst = collections.namedtuple('Inst', ('dir', 'num'))
instructions = [Inst(line[0], int(line[1:])) for line in read_data()]

def run():
    waypoint = V(10, -1)
    pos = V()
    N = V(0, -1)
    E = V(1, 0)
    S = V(0, 1)
    W = V(-1, 0)

    for inst in instructions:
        print(inst)
        if inst.dir == 'F':
            pos += waypoint * inst.num
        elif inst.dir == 'L':
            waypoint = waypoint.ccw(int(inst.num / 90))
        elif inst.dir == 'R':
            waypoint = waypoint.cw(int(inst.num / 90))
        elif inst.dir == 'N':
            waypoint += N * inst.num
        elif inst.dir == 'E':
            waypoint += E * inst.num
        elif inst.dir == 'S':
            waypoint += S * inst.num
        elif inst.dir == 'W':
            waypoint += W * inst.num
        else:
            assert False
        print(pos, waypoint)
        # input()
    return pos.manhattan

answer = run()
print(answer)
if len(sys.argv) > 0:
    sys.exit(0)
from aocd import submit
submit(answer, part="a", day=12, year=2020)
