#!/usr/bin/env python

from util import *

INPUT_RE = re.compile(r'(\d+)-(\d+) (\w): (.*)')
rows = []

Row = collections.namedtuple('password', ('min_occur', 'max_occur', 'letter', 'password'))

with open(sys.argv[1], 'r') as f:
    for line in f:
        rows.append(Row(*INPUT_RE.match(line).groups()))

def is_valid(row):
    counts = collections.defaultdict(lambda: 0)
    for char in row.password:
        counts[char] += 1
    if counts[row.letter] < int(row.min_occur):
        return False
    if counts[row.letter] > int(row.max_occur):
        return False
    return True

print(len([row for row in rows if is_valid(row)]))
