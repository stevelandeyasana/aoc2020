#!/usr/bin/env python

from util import *

numbers = [int(line.strip()) for line in read_data()]

sorted_numbers = sorted(numbers)
# print(sorted_numbers)
num_one = 0
num_three = 1

if sorted_numbers[0] == 1:
    num_one += 1
if sorted_numbers[0] == 3:
    num_three += 1
for i, n in enumerate(sorted_numbers[:-1]):
    n2 = sorted_numbers[i + 1]
    if n2 - n == 1:
        num_one += 1
    elif n2 - n == 3:
        num_three += 1

# answer = num_one * num_three


print("running...")
sorted_numbers = [0] + sorted_numbers + [sorted_numbers[-1] + 3]
print(sorted_numbers)

nexts = [[] for _ in sorted_numbers]

for i in range(0, len(sorted_numbers) - 1):
    j = i + 1
    while j < len(sorted_numbers) and sorted_numbers[j] - sorted_numbers[i] <= 3:
        nexts[i].append(j)
        j += 1
for i, n in enumerate(sorted_numbers):
    print("{}: {} => {}".format(i, n, repr([sorted_numbers[k] for k in nexts[i]])))

lut = [None for _ in nexts]
def run(i):
    if not nexts[i]:
        return 1
    if lut[i] is None:
        lut[i] = 0
        for nxt in nexts[i]:
            lut[i] += run(nxt)
    return lut[i]

answer = run(0)

print(answer)
# sys.exit(0)
from aocd import submit
submit(answer, part="b", day=10, year=2020)
