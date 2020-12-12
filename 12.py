#!/usr/bin/env python

from util import *

Inst = collections.namedtuple('Inst', ('dir', 'num'))
instructions = [Inst(line[0], int(line[1:])) for line in read_data()]

def cw(delta):
    return [-delta[1], delta[0]]

def ccw(delta):
    return [delta[1], -delta[0]]

def sub(a, b):
    return [a[0] - b[0], a[1] - b[1]]

def add(a, b, mult=1):
    return [a[0] + b[0] * mult, a[1] + b[1] * mult]

def run():
    waypoint = [10, -1]
    pos = [0, 0]

    def move_waypoint(x, y, amt):
        nonlocal waypoint
        waypoint[0] += x * amt
        waypoint[1] += y * amt

    for inst in instructions:
        print(inst)
        if inst.dir == 'F':
            pos = add(pos, waypoint, inst.num)
        elif inst.dir == 'L':
            for _ in range(0, int(inst.num / 90)):
                waypoint = ccw(waypoint)
        elif inst.dir == 'R':
            for _ in range(0, int(inst.num / 90)):
                waypoint = cw(waypoint)
        elif inst.dir == 'N':
            move_waypoint(0, -1, inst.num)
        elif inst.dir == 'E':
            move_waypoint(1, 0, inst.num)
        elif inst.dir == 'S':
            move_waypoint(0, 1, inst.num)
        elif inst.dir == 'W':
            move_waypoint(-1, 0, inst.num)
        else:
            assert False
        print(pos, waypoint)
        # input()
    return abs(pos[0]) + abs(pos[1])

answer = run()
print(answer)
sys.exit(0)
from aocd import submit
submit(answer, part="a", day=12, year=2020)
