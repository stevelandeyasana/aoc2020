#!/usr/bin/env python

from util import *

INPUT_RE = re.compile(r'(\d+)-(\d+) (\w): (.*)')
rows = []
Row = collections.namedtuple('password', ('first_char_ix', 'second_char_ix', 'char', 'password'))

for line in read_data():
    rows.append(Row(*INPUT_RE.match(line).groups()))

def is_valid(row):
    if row.password[int(row.first_char_ix) - 1] == row.char:
        return row.password[int(row.second_char_ix) - 1] != row.char
    if row.password[int(row.second_char_ix) - 1] == row.char:
        return row.password[int(row.first_char_ix) - 1] != row.char
    return False

print(len([row for row in rows if is_valid(row)]))
