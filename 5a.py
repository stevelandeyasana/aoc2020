#!/usr/bin/env python

from util import *

def bisect_lower(range):
    assert (range[1] - range[0]) % 2 == 0
    return (range[0], range[0] + (range[1] - range[0]) / 2)

def bisect_upper(range):
    assert (range[1] - range[0]) % 2 == 0
    return (range[0] + (range[1] - range[0]) / 2, range[1])

assert bisect_lower((0, 128)) == (0, 64)
assert bisect_upper((0, 128)) == (64, 128)

def process(line):
    z_range = (0, 128) # incl, excl
    x_range = (0, 8) # incl, excl

    for char in line[0:7]:
        if char == 'F': # take lower half
            z_range = bisect_lower(z_range)
        elif char == 'B': # take upper half
            z_range = bisect_upper(z_range)
        else:
            raise ValueError("You have a bug: {}, {}".format(line, char))
    for char in line[7:]:
        if char == 'L': # take lower half
            x_range = bisect_lower(x_range)
        elif char == 'R': # take upper half
            x_range = bisect_upper(x_range)
        else:
            raise ValueError("You have a bug: {}, {}".format(line, char))
    return int(z_range[0]), int(x_range[0])

def calc_id(coords):
    return coords[0] * 8 + coords[1]

max_id = 0
for line in read_data():
    max_id = max(max_id, calc_id(process(line.rstrip())))
print(max_id)

all_numbers = set(range(0, 916))

for line in read_data():
    id = calc_id(process(line.rstrip()))
    all_numbers.remove(id)
print(all_numbers)

# print(process('FBFBBFFRLR'))

# for line in read_data():
#     rows.append(Row(*INPUT_RE.match(line).groups()))

# from aocd import submit
# submit(answer, part="a", day=3, year=2020)