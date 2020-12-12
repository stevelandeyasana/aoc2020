#!/usr/bin/env python

import sys
from aocd import submit

val = sys.stdin.read()
if val.strip() == 'fail':
    sys.exit(1)
submit(int(val), part=sys.argv[2], day=int(sys.argv[1]), year=2020)