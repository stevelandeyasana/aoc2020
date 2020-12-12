#!/usr/bin/env python

from util import *

def process(line):
    return int(line.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), 2)

max_id = 0
for line in read_data():
    max_id = max(max_id, process(line.rstrip()))
print(max_id)

all_numbers = set(range(0, 916))

for line in read_data():
    id = process(line.rstrip())
    all_numbers.remove(id)
print(all_numbers)