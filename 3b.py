#!/usr/bin/env python

from util import *

INPUT_RE = re.compile(r'(\d+)-(\d+) (\w): (.*)')
rows = []
Row = collections.namedtuple('password', ('first_char_ix', 'second_char_ix', 'char', 'password'))

for line in read_data():
    rows.append(Row(*INPUT_RE.match(line).groups()))

# from aocd import submit
# submit(answer, part="a", day=3, year=2020)