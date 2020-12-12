#!/usr/bin/env python

from util import *

val = 0
for g in read_multiline_groups(join_str=None):
    val += len(set.intersection(*map(set, g)))
print(val)

# from aocd import submit
# submit(answer, part="a", day=3, year=2020)