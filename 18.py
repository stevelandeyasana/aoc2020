#!/usr/bin/env python

from util import *

PART = "a"

def parse(line):
    return (c for c in line if c.strip())

def eval(iter):
    result = None
    op = None

    def apply_op(subexpr):
        nonlocal result
        nonlocal op
        print(result, op, subexpr)
        if op is None:
            result = subexpr
        elif op == '+':
            result += subexpr
        elif op == '-':
            result -= subexpr
        elif op == '*':
            result *= subexpr
        elif op == '/':
            result /= subexpr
        else:
            assert False
        op = 'error'
        print('=>', result)

    while True:
        try:
            char = next(iter)
            print(char)
        except StopIteration:
            print('end with', result)
            return result
        if char == ')':
            print('pop with', result)
            return result
        elif char == '(':
            print('push')
            subexpr = eval(iter)
            apply_op(subexpr)
        elif char in ('+', '-', '*', '/'):
            print('set op')
            op = char
        else:
            subexpr = int(char)
            apply_op(subexpr)


# assert eval(parse('1 + 2 * 3 + 4 * 5 + 6')) == 71
# assert eval(parse('1 + (2 * 3) + (4 * (5 + 6))')) == 51

def run():
    return sum(eval(parse(line)) for line in read_data())

# answer = run()

def parse2(line):
    def gen():
        for c in line:
            if c.strip():
                try:
                    yield int(c)
                except ValueError:
                    yield c
    return list(gen())


def iter(expr, allow_add, allow_mul, start=0):
    for i in range(start, len(expr) - 2):
        a = expr[i]
        b = expr[i + 1]
        c = expr[i + 2]
        if isinstance(a, int) and isinstance(c, int) and allow_mul and b in ('*', '/'):
            # if b == '*'
            val = a * c
            if b == '/':
                val = a / c
            return expr[0:i] + [val] + expr[i+3:]
        elif isinstance(a, int) and isinstance(c, int) and allow_add and b in ('+', '-'):
            # if b == '+'
            val = a + c
            if b == '-':
                val = a - c
            return expr[0:i] + [val] + expr[i+3:]
        elif a == '(' and isinstance(b, int) and c == ')':
            return expr[0:i] + [b] + expr[i+3:]
    return expr


def _eval(expr):
    if len(expr) == 1:
        if isinstance(expr[0], list):
            return _eval(expr[0])

    for i in range(0, len(expr)):
        if isinstance(expr[i], list):
            expr[i] = _eval(expr[i])

    did_change = True
    while did_change:
        did_change = False
        for i in range(0, len(expr) - 2):
            a = expr[i]
            op = expr[i + 1]
            b = expr[i + 2]
            if op == '+':
                did_change = True
                expr = expr[0:i] + [a + b] + expr[i+3:]
                break
            elif op == '-':
                did_change = True
                expr = expr[0:i] + [a - b] + expr[i+3:]
                break
        
    did_change = True
    while did_change:
        did_change = False
        for i in range(0, len(expr) - 2):
            a = expr[i]
            op = expr[i + 1]
            b = expr[i + 2]
            if op == '*':
                did_change = True
                expr = expr[0:i] + [a * b] + expr[i+3:]
                break
            elif op == '/':
                did_change = True
                expr = expr[0:i] + [a / b] + expr[i+3:]
                break
    assert len(expr) == 1
    return expr[0]


def eval3(expr):
    nested = []
    list_stack = [nested]
    for c in expr:
        if c == '(':
            new_list = []
            list_stack[-1].append(new_list)
            list_stack.append(new_list)
        elif c == ')':
            list_stack.pop()
        else:
            list_stack[-1].append(c)

    print(nested)

    return _eval(nested)


assert eval3(parse2('2 * 3 + (4 * 5)')) == 46
assert eval3(parse2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')) == 23340

sys.exit(0)

def run2():
    return sum(eval3(parse2(line)) for line in read_data())
answer = run2()

PART = "b"

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=18, year=2020)
