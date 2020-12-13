#!/usr/bin/env python

from util import *

line_iter = read_data()
ts = int(next(line_iter))

buses = [int(x) for x in next(line_iter).split(',') if x != 'x']

print(ts, buses)

def run():
    best_delta = ts
    bus2 = buses[0]
    amt2 = 1
    for bus in buses:
        amt = int(ts / bus)
        val = amt * bus
        if val == ts:
            return bus, amt
        amt += 1
        val += bus
        delta = val - ts
        if delta < best_delta:
            best_delta = delta
            bus2 = bus
            amt2 = amt
    return (bus2, amt2)

bus, amt = run()
wait = bus * amt - ts
answer = wait * bus
print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part="b", day=13, year=2020)
