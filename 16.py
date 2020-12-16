#!/usr/bin/env python

from util import *

PART = "a"

@attr.s
class Constraint:
    a = attr.ib()
    b = attr.ib()
    name = attr.ib()

constraints = {}
tickets = []

def parse_range(r):
    a, b = r.split('-')
    return (int(a), int(b))

state = 'constraints'
iter = read_data()
for line in iter:
    if not line.strip():
        if state == 'constraints':
            state = 'yours'
            next(iter)
        elif state == 'yours':
            state = 'nearby'
            next(iter)
        else:
            assert False
        continue
    if state == 'constraints':
        k, v = line.strip().split(": ")
        ranges = v.split(' or ')
        constraints[k] = Constraint(name=k, a=parse_range(ranges[0]), b=parse_range(ranges[1]))
    elif state == 'yours':
        continue
    elif state == 'nearby':
        tickets.append([int(x) for x in line.strip().split(',')])


def check_one(value, constraint):
    print(value, 'in', constraint.a, constraint.b, '?')
    if value >= constraint.a[0] and value <= constraint.a[1]:
        return True
    if value >= constraint.b[0] and value <= constraint.b[1]:
        return True
    return False


def check(ticket):
    for value in ticket:
        had_success = False
        for constraint in constraints.values():
            if check_one(value, constraint):
                had_success = True
        if not had_success:
            yield value


# print(constraints)
# answer = 0
# for ticket in tickets:
#     print(ticket)
#     for invalid_value in check(ticket):
#         answer += invalid_value

PART = "b"


def check2(ticket):
    for value in ticket:
        had_success = False
        for constraint in constraints.values():
            if check_one(value, constraint):
                had_success = True
                break
        if not had_success:
            return False
    return True

tickets = [t for t in tickets if check2(t)]
print('tickets:', tickets)

allowed_indices = {}

def test(k, constraint, i):
    for t in tickets:
        if not check_one(t[i], constraint):
            allowed_indices[k].remove(i)
            return

for k, c in constraints.items():
    allowed_indices[k] = {i for i in range(len(constraints))}
    for i in range(len(constraints)):
        test(k, c, i)

# print(dict(allowed_indices))

final_constraints = [None for _ in range(len(constraints))]
resolution_order = sorted(constraints.values(), key=lambda c: len(allowed_indices[c.name]))
for c in resolution_order:
    i = allowed_indices[c.name].pop()
    for aiv in allowed_indices.values():
        if i in aiv:
            aiv.remove(i)
    final_constraints[i] = c

print(final_constraints)
    
answer = 1
my_ticket = (89,139,79,151,97,67,71,53,59,149,127,131,103,109,137,73,101,83,61,107)
for i in range(len(final_constraints)):
    if final_constraints[i].name.startswith('departure'):
        answer *= my_ticket[i]

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=16, year=2020)
