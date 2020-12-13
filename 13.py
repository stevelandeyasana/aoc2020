#!/usr/bin/env python

from util import *

line_iter = read_data()
ts = int(next(line_iter))

@attr.s
class Bus:
    offset = attr.ib()
    num = attr.ib()
    t = attr.ib()

values = next(line_iter).split(',')
buses = [Bus(offset=i, t=0, num=int(x) if x != 'x' else None) for i, x in enumerate(values) if x != 'x']

print(buses)

def check(t, my_buses=buses):
    for bus in my_buses:
        actual_t = t + bus.offset
        if actual_t % bus.num != 0:
            return False
    return True

def run():
    t = 0
    period = 1
    for i, bus in enumerate(buses):
        while not check(t, buses[0:i + 1]):
            t += period
        period *= bus.num
    return t


answer = run()

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part="b", day=13, year=2020)
