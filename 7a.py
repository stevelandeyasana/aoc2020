#!/usr/bin/env python

from util import *

RE = re.compile(r'^(.*) bags contain (.*)\.$')
RE2 = re.compile('(\d+) (.*) bags?')

def parse(lol):
    if lol == 'no other bags':
        return None
    m = RE2.match(lol)
    assert m
    return (int(m.group(1)), m.group(2))

items = {}
for line in read_data():
    m = RE.match(line)
    assert m
    src = m.group(1)
    dests = [parse(d) for d in m.group(2).split(', ') if parse(d) is not None]
    items[src] = dests

print(items)

# points_to = set(['shiny gold'])
# len_before = len(points_to)
# while True:
#     for src, dests in items:
#         for count, label in dests:
#             if label in points_to:
#                 print("{} => {}".format(src, label))
#                 points_to.add(src)
#     if len_before == len(points_to):
#         break
#     len_before = len(points_to)

def traverse(bag):
    n = 1
    for (num, subbag) in items[bag]:
        n += traverse(subbag) * num
    return n

print(traverse('shiny gold') - 1)


from aocd import submit
submit(answer, part="b", day=7, year=2020)