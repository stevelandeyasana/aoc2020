#!/usr/bin/env python

from util import *

rows = []
for line in read_data():
    rows.append(list(line.strip()))

def get_counts(delta):
    pos = (0, 0)
    trees_count = 0
    while pos[1] < len(rows):
        (x, y) = pos
        row = rows[y]
        if row[x % len(row)] == '#':
            # row[x] = 'X'
            trees_count += 1
        # else:
        #     row[x] = 'O'
        # print(''.join(row))
        pos = (x + delta[0], y + delta[1])
    print(trees_count)
    return trees_count

product = 1
product *= get_counts((1, 1))
product *= get_counts((3, 1))
product *= get_counts((5, 1))
product *= get_counts((7, 1))
product *= get_counts((1, 2))

print(product)
# from aocd import submit
# submit(product, part="b", day=3, year=2020)