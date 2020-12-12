#!/usr/bin/env python
import sys
import util

numbers = set(util.numbers_from_file(sys.argv[1]))

for n in numbers:
    if (2020 - n) in numbers:
        print(n *  (2020 -n))
        sys.exit(0)
