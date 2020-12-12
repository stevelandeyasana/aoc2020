#!/usr/bin/env python

from util import *

req_fields = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid')

CM_RE = re.compile('^(\d+)cm$')
IN_RE = re.compile('^(\d+)in$')
HAIR_RE = re.compile('^#[a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9]$')
PID_RE = re.compile('^\d\d\d\d\d\d\d\d\d$')
def process(vals):
    missing_fields = set(req_fields) - set(vals.keys())

    if len(missing_fields) == 1 and 'cid' in missing_fields:
        pass
    elif len(missing_fields) == 0:
        pass
    else:
        return False

    try:
        if int(vals['byr']) < 1920 or int(vals['byr']) > 2002:
            return False
    except ValueError:
        return False

    try:
        if int(vals['iyr']) < 2010 or int(vals['iyr']) > 2020:
            return False
    except ValueError:
        return False

    try:
        if int(vals['eyr']) < 2020 or int(vals['eyr']) > 2030:
            return False
    except ValueError:
        return False

    try:
        cm_match = CM_RE.match(vals['hgt'])
        in_match = IN_RE.match(vals['hgt'])
        if cm_match:
            n = int(cm_match.group(1))
            if n < 150 or n > 193:
                return False
        elif in_match:
            n = int(in_match.group(1))
            if n < 59 or n > 76:
                return False
        else:
            return False
    except ValueError:
        return False

    if not HAIR_RE.match(vals['hcl']):
        return False

    if not vals['ecl'] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
        return False

    if not PID_RE.match(vals['pid']):
        return False

    return True

def main():
    num_valid = 0
    for line in read_multiline_groups(join_str=' '):
        vals = {}
        pair_strs = line.strip().split(' ')
        for pair_str in pair_strs:
            k, v = pair_str.split(':')
            vals[k] = v
        num_valid += 1 if process(vals) else 0
    print(num_valid)

main()

# from aocd import submit
# submit(answer, part="a", day=3, year=2020)
