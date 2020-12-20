#!/usr/bin/env python

from util import *

PART = "a"

def list2expr(rules, k, cache):
    subexprs = []
    if k in cache:
        return cache[k]
    for item in rules[k]:
        if len(item) == 1 and '"' in item[0]:
            cache[k] = item[0].replace('"', '')
            return cache[k]
        else:
            subexprs.append(''.join([list2expr(rules, subitem, cache) for subitem in item]))
    cache[k] = '(' + '|'.join(subexprs) + ')'
    return cache[k]

# _cache={}
# assert list2expr({'0': [['"a"']], '1': [['0', '0', '0'], ['0', '0', '0']]}, '1', _cache) == '(aaa|aaa)'


def _run(path=None):
    rules = {}
    cache = {}
    iter = read_data(path)
    while True:
        line = next(iter)
        if not line.strip():
            break
        k, v = line.strip().split(': ', 1)
        options = v.split(' | ')
        rules[k] = [o.split(' ') for o in options]
    exprs = {k: list2expr(rules, k, cache) for k in rules.keys()}
    print(rules)
    print(exprs)
    result = 0
    for line in iter:
        if re.match('^' + exprs['0'] + '$', line.strip()):
            print("Match:", line.strip())
            result += 1
        else:
            print("No match:", line.strip())
    return result

PART = "b"

def run2(path):
    return run(path)
    rules, lines = get_rules_and_iter(path)

# assert run2('19ex3.txt') == 3
answer = _run('19.txt')


print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=19, year=2020)
