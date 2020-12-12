#!/usr/bin/env python

from util import *

# KV_RE = re.compile(r'([^\s]+):([^\s]+)\s*')
INPUT_RE = re.compile(r'(\d+)-(\d+) (\w): (.*)')
rows = []

req_fields = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid')
Passport = collections.namedtuple('Passport', ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'))

def process(passport):
    pass

num_valid = 0
vals = {}
missing_fields = set(req_fields)

def process():
    global vals
    global missing_fields
    global num_valid
    print("collect", vals)
    if len(missing_fields) == 1 and 'cid' in missing_fields:
        # print("valid minus cid")
        num_valid += 1
    elif len(missing_fields) == 0:
        num_valid += 1
        # print("valid")
    else:
        # print("Missing", missing_fields)
        pass
    vals = {}
    missing_fields = set(req_fields)

for line in read_data():
    if line.strip():
        pair_strs = line.split(' ')
        for pair_str in pair_strs:
            k, v = pair_str.split(':')
            missing_fields.remove(k)
            vals[k] = v
    else:
        process()
process()

print(num_valid)
# from aocd import submit
# submit(answer, part="a", day=3, year=2020)
