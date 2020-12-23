#!/usr/bin/env python

from util import *

PART = "a"

CUPS = [int(c) for c in list(read_data())[0] if c in '1234567890']

"""
def iter_cups(cups, i):
    min_cup = min(*cups)
    max_cup = max(*cups)
    print(cups)
    print('curr:', cups[i])
    current = cups[i]
    picked_up = cups[i+1:i+4]
    cups[i+1:i+4] = []
    dest_cup = current - 1
    if dest_cup < min_cup:
        dest_cup = max_cup
    print(picked_up, dest_cup)
    while dest_cup in picked_up or dest_cup == current:
        # print('look for', dest_cup, 'in', cups)
        dest_cup -= 1
        if dest_cup < min_cup:
            dest_cup = max_cup
    dest_cup_ix = cups.index(dest_cup)
    print('dest:', dest_cup)
    print('  at', dest_cup_ix)

    cups[dest_cup_ix+1:dest_cup_ix+1] = picked_up
    print("=>", cups)
    return cups

    # if dest_cup_ix == 0:
    #     return [remaining[dest_cup_ix]] + picked_up + remaining[dest_cup_ix+1:] + [current]
    # elif dest_cup_ix < len(remaining) - 1:
    # result = [remaining[dest_cup_ix]] + picked_up + remaining[dest_cup_ix+1:] + remaining[0:dest_cup_ix] + [current]
    # print([remaining[dest_cup_ix]], picked_up, remaining[dest_cup_ix+1:], remaining[0:dest_cup_ix], [current])
    # result = [remaining[dest_cup_ix]] + picked_up + remaining[dest_cup_ix+1:] + remaining[0:dest_cup_ix] + [current]
    # print("=>", result)
    # return result
    # else:
    #     return [remaining[dest_cup_ix]] + picked_up + remaining[0:dest_cup_ix] + [current]

def go(cups, n_max=100, is_a=True):
    for n in range(0, n_max):
        print(n)
        # print('----\nmove', n+1)
        cups = iter_cups(cups, n)
    one_ix = cups.index(1)
    result_cups = cups[one_ix+1:] + cups[0:one_ix]
    # print("final:", result_cups)
    # print(''.join([str(i) for i in result_cups]))
    if is_a:
        return ''.join([str(i) for i in result_cups])
    else:
        return result_cups[0] * result_cups[1]

def run(path):
    return go([int(c) for c in list(read_data(path=path))[0] if c in '1234567890'])

"""

CACHE = {}

@attr.s
class Node:
    val = attr.ib()
    nxt = attr.ib(default=lambda: None)
    prv = attr.ib(default=lambda: None)

    def find(self, val):
        return CACHE[val]
        # for node in self:
        #     if node.val == val:
        #         return node
        # raise IndexError()

    def insert_after(self, node):
        old_nxt = self.nxt
        self.nxt = node
        node.prv = self
        node.nxt = old_nxt
        old_nxt.prv = node

    def insert_n_after(self, nodes):
        cursor = self
        for node in nodes:
            cursor.insert_after(node)
            cursor = node

    def remove_next(self):
        removed = self.nxt
        self.nxt = removed.nxt
        self.nxt.prv = self
        return removed

    def remove_n_after(self, n):
        result = []
        while len(result) < n:
            result.append(self.remove_next())
        return result

    def __iter__(self):
        yield self
        cursor = self.nxt
        while cursor is not self:
            yield cursor
            cursor = cursor.nxt

    def __str__(self):
        l = [self.val]
        cursor = self.nxt
        while cursor is not self:
            l.append(cursor.val)
            cursor = cursor.nxt
        return repr(l)

    def __repr__(self):
        l = [self.val]
        cursor = self.nxt
        while cursor is not self:
            l.append(cursor.val)
            cursor = cursor.nxt
        return repr(l)

def make_ring(cups):
    root = Node(val=cups[0])
    CACHE[root.val] = root
    last = root
    for i in range(1, len(cups)):
        node = Node(val=cups[i], prv=last)
        CACHE[node.val] = node
        last.nxt = node
        last = node
    node.nxt = root
    root.prv = node 
    return root

def iter_cups(node, min_cup, max_cup):
    # print("  on", node.val)
    picked_up = node.remove_n_after(3)
    # print("  picked up", [n.val for n in picked_up])
    dest_cup = node.val - 1
    if dest_cup < min_cup:
        dest_cup = max_cup
    disallowed = [node.val for node in picked_up]
    while dest_cup in disallowed or dest_cup == node.val:
        # print('look for', dest_cup, 'in', cups)
        dest_cup -= 1
        if dest_cup < min_cup:
            dest_cup = max_cup
    # print("  dest:", dest_cup)
    cursor = node.find(dest_cup)
    cursor.insert_n_after(picked_up)
    # print("  result:", node)
    return node.nxt

def test_cups(cups, start_ix):
    min_cup = cups[0]
    max_cup = cups[0]
    root = make_ring(cups)
    for node in root:
        min_cup = min(min_cup, node.val)
        max_cup = max(max_cup, node.val)
    print("TEST", root)
    for _ in range(0, start_ix):
        root = root.nxt
    iter_cups(root, min_cup, max_cup)
    result = [node.val for node in root]
    for _ in range(0, start_ix):
        result[0:0] = [result[-1]]
        result[-1:] = []
    print("rotated:", result)
    return result

print(make_ring([3, 8, 9, 1, 2, 5, 4, 6, 7]))
assert test_cups([3, 8, 9, 1, 2, 5, 4, 6, 7], 0) == [3,2,8,9,1,5,4,6,7]
assert test_cups([3, 2,8,9,1,5,4,6,7], 1) == [3,2,5,4,6,7,8,9,1]
assert test_cups([3,2, 5,4,6,7,8,9,1], 2) == [7,2,5,8,9,1,3,4,6]
print("asserts pass")
# print(repr(go([3,8,9,1,2,5,4,6,7])))

def go(initial, n_max=10, is_a=True):
    root = make_ring(initial)
    min_cup = root.val
    max_cup = root.val
    for node in root:
        min_cup = min(min_cup, node.val)
        max_cup = max(max_cup, node.val)

    node = root
    for n in range(0, n_max):
        # print(node)
        if n % 100000 == 0:
            print(n)
        # print('----\nmove', n+1)
        node = iter_cups(node, min_cup, max_cup)
    # print(node)
    if is_a:
        node = node.find(1)
        print(''.join([str(i.val) for i in node])[1:])
        return ''.join([str(i.val) for i in node])[1:]
    else:
        one = node.find(1)
        return one.nxt.val * one.nxt.nxt.val
    

assert go([3,8,9,1,2,5,4,6,7]) == '92658374'

# answer = run('23.txt')

MILL_CUPS = [] + CUPS
next_cup = max(*CUPS) + 1
print("priming da cups")
while len(MILL_CUPS) < 1_000_000:
    MILL_CUPS.append(next_cup)
    next_cup += 1

answer = go(MILL_CUPS, n_max=10_000_000, is_a=False)

assert isinstance(answer, int)
assert answer != None
assert answer != 0
assert answer != ''

PART = "b"

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=23, year=2020)
