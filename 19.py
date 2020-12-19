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

def poss_str(k, item):
    return '{}-{}'.format(k, ','.join(item))


def eval(rules, k, s, i, used_possibilities, indent=''):
    if i == 0:
        # print(rules)
        print('check', repr(s))
    if i >= len(s):
        print(indent, 'end of string')
        return (False, i)
    print(indent, repr(k), 'at', i, repr(s[i]))
    if isinstance(rules[k], str):
        if s[i] == rules[k]:
            print(indent, 'match', rules[k])
            return (True, i + 1)
        else:
            print(indent, 'fail', rules[k])
            return (False, i)

    sub_poss = set(used_possibilities)
    i_before = i
    for possibility in rules[k]:
        print(indent, 'test', possibility)
        dedup_k = poss_str(k, possibility)
        # if dedup_k in used_possibilities:
        #     print(indent, 'XXX duplicate')
        #     continue
        sub_poss.add(dedup_k)
        is_ok = True
        for rule_key in possibility:
            is_ok, i = eval(rules, rule_key, s, i, sub_poss, indent+'  ')
            if not is_ok: break
        if is_ok:
            print(indent, 'pass')
            # used_possibilities.add(dedup_k)
            if i_before == 0 and i < len(s):
                return (False, i_before)
            else:
                return (True, i)
        else:
            i = i_before
        sub_poss.remove(dedup_k)

    return (False, i)


def get_rules_and_iter(path=None):
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
        if len(rules[k]) == 1 and '"' in rules[k][0][0]:
            rules[k] = rules[k][0][0][1:-1]

    return rules, iter

def check_line(rules, line):
    print(rules)
    is_ok, _ = eval(rules, '0', line.strip(), 0, set())
    return is_ok

def run(path):
    rules, lines = get_rules_and_iter(path)
    return sum(1 if check_line(rules, line) else 0 for line in lines)

rules, lines = get_rules_and_iter('19ex.txt')
print(rules)
assert check_line(rules, 'ababbb') == True
assert check_line(rules, 'bababa') == False
assert check_line(rules, 'abbbab') == True
assert check_line(rules, 'aaabbb') == False
assert check_line(rules, 'aaaabbb') == False

# sys.exit(0)
answer = _run('19ex.txt')
print(answer)
assert answer == 2

answer = _run('19.txt')
assert answer != 0

# PART = "b"

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=19, year=2020)
