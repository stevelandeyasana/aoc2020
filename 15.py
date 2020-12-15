#!/usr/bin/env python

from util import *

PART = "a"

numbers = [int(x) for x in next(read_data()).split(',')]
print(numbers)

memory = {}

last = None

for i in range(30000000):
    if i % 100000 == 0:
        print(i)
    val = None
    if i < len(numbers):
        memory[numbers[i]] = [i]
        last = numbers[i]
        continue

    # print()
    # print(i)

    if not memory.get(last, None):
        memory[last] = []
    
    if len(memory[last]) < 2:
        last = 0
    else:
        delta = memory[last][-1] - memory[last][-2]
        last = delta
    # print(last)
    if not memory.get(last, None):
        memory[last] = []
    memory[last].append(i)

    if len(memory[last]) > 2:
        memory[last] = memory[last][-2:]
    # print(memory)

answer = last

PART = "b"

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=15, year=2020)
