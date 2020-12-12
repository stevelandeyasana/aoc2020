import collections
import re
import sys
import attr
from aocd import get_data, submit

def numbers_from_file(path):
    with open(path, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]

def read_data():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            yield from f
    else:
        num = re.match(r'.*[^\d](\d+)[^\d]', sys.argv[0]).group(1)
        with open(num + '.txt', 'r') as f:
            yield from f

def read_multiline_groups(join_str=None):
    lines = []
    for line in read_data():
        if lines and not line.strip():
            if join_str is not None:
                yield join_str.join(lines)
            else:
                yield lines
            lines = []
        elif line.strip():
            lines.append(line.rstrip())
    if lines:
        if join_str is not None:
            yield join_str.join(lines)
        else:
            yield lines

class Grid:
    def __init__(self, lines=None, w=None, h=None, cells=None):
        self.cells = {}
        self.h = 0
        if lines is not None:
            for line in lines:
                self.w = len(line)
                for x in range(0, len(line)):
                    self.cells[(x, self.h)] = line[x]
                self.h += 1
        if w is not None:
            self.w = w
        if h is not None:
            self.h = h
        if cells is not None:
            self.cells = cells

    def __getitem__(self, k):
        return self.cells.get(k, None)

    def get(self, x, y):
        return self[(x, y)]

    def __setitem__(self, k, val):
        self.cells[k] = val
    
    def set(self, x, y, val):
        self.cells[(x, y)] = val

    def copy(self):
        return Grid(w=self.w, h=self.h, cells={k: v for k, v in self.cells.items()})

    @property
    def coords(self):
        for y in range(0, self.h):
            for x in range(0, self.w):
                yield (x, y)

    def neighbor(self, coord, delta, oops=None):
        if oops is not None:
            d2 = oops
            coord = (coord, delta)
            delta = d2
        return self.cells.get((coord[0] + delta[0], coord[1] + delta[1]), None)

    def print(self):
        for y in range(0, self.h):
            print(''.join([self[(x, y)] for x in range(0, self.w)]))
        print()

    def __eq__(self, g2):
        if self.w != g2.w:
            return False
        if self.h != g2.h:
            return False
        for coord in self.coords:
            if self[coord] != g2[coord]:
                return False
        return True
