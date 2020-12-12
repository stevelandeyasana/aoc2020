#!/usr/bin/env python
import sys
import util

numbers = set(util.numbers_from_file(sys.argv[1]))

def find_sum(val):
    for n in numbers:
        if (val - n) in numbers:
            return n, val - n
    return None

def product_of_three():
    for n in numbers:
        result = find_sum(2020 - n)
        if result is None:
            continue
        print(n * result[0] * result[1])
        return
        
product_of_three()
