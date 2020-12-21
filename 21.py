#!/usr/bin/env python

from util import *

PART = "a"

@attr.s
class Food:
    ingredients = attr.ib()
    allergens = attr.ib()

def parse(path=None):
    FOOD_RE = re.compile(r'([^(]+) \(contains ([^)]+)')
    for line in read_data(path=path):
        m = FOOD_RE.match(line.strip())
        yield Food(
            ingredients=m.group(1).split(' '),
            allergens=m.group(2).split(', '))

def run(path=None):
    allergen_possibilities = {}
    foods = list(parse(path=path))
    all_ingredients = set()
    for food in foods:
        all_ingredients |= set(food.ingredients)
        for allergen in food.allergens:
            if allergen not in allergen_possibilities:
                allergen_possibilities[allergen] = set(food.ingredients)
            else:
                allergen_possibilities[allergen] = set.intersection(allergen_possibilities[allergen], food.ingredients)

    all_allergen_possibilities = set()
    for poss in allergen_possibilities.values():
        all_allergen_possibilities |= poss

    result = all_ingredients - all_allergen_possibilities
    return result

def run2(path=None):
    allergen_possibilities = {}
    foods = list(parse(path=path))
    all_ingredients = set()
    for food in foods:
        all_ingredients |= set(food.ingredients)
        for allergen in food.allergens:
            if allergen not in allergen_possibilities:
                allergen_possibilities[allergen] = set(food.ingredients)
            else:
                allergen_possibilities[allergen] = set.intersection(allergen_possibilities[allergen], food.ingredients)

    assigned_allergens = {}

    len_before = len(allergen_possibilities)
    while allergen_possibilities:
        pprint(allergen_possibilities)
        for allergen, possibilities in allergen_possibilities.items():
            print('check', allergen, possibilities)
            if len(possibilities) == 1:
                print('solve', allergen)
                value = possibilities.pop()
                assigned_allergens[allergen] = value
                del allergen_possibilities[allergen]
                for a2, poss2 in allergen_possibilities.items():
                    allergen_possibilities[a2] = poss2 - {value}
                break
        if len(allergen_possibilities) == len_before:
            sys.exit(1)
        len_before = len(allergen_possibilities)

    return ','.join([assigned_allergens[k] for k in sorted(list(assigned_allergens.keys()))])

PART = "b"

assert run2('21ex.txt') == 'mxmxvkd,sqjhc,fvjkl'
assert run('21ex.txt') == {'kfcds', 'nhms', 'sbzzf', 'trh'}

print("---")

def tally(results):
    num = 0
    for food in parse():
        for ingredient in results:
            if ingredient in food.ingredients:
                num += 1
    return num

answer = run2()
assert answer != None
assert answer != 0
assert answer != ''

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=21, year=2020)
