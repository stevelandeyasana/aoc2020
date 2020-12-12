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
    def __init__(self, lines=None, size=None, cells=None):
        self.cells = {}
        self.size = V()
        if lines is not None:
            for line in lines:
                self.size.x = len(line)
                for x in range(0, len(line)):
                    self.cells[V(x, self.size.y)] = line[x]
                self.size.y += 1
        if size is not None:
            self.size = size
        if cells is not None:
            self.cells = cells

    def __getitem__(self, k):
        assert isinstance(k, Vector2)
        return self.cells.get(k, None)

    def get(self, x, y):
        return self[V(x, y)]

    def __setitem__(self, k, val):
        assert isinstance(k, Vector2)
        self.cells[k] = val
    
    def set(self, x, y, val):
        self.cells[V(x, y)] = val

    def copy(self):
        return Grid(size=self.size, cells={k: v for k, v in self.cells.items()})

    @property
    def coords(self):
        for y in range(0, self.size.y):
            for x in range(0, self.size.x):
                yield V(x, y)

    def neighbor(self, coord, delta, oops=None):
        if oops is not None:
            d2 = oops
            coord = V(coord, delta)
            delta = d2
        return self.cells.get(coord + delta, None)

    def print(self):
        for y in range(0, self.size.y):
            print(''.join([self[V(x, y)] for x in range(0, self.size.x)]))
        print()

    def __eq__(self, g2):
        if self.size != g2.size:
            return False
        for coord in self.coords:
            if self[coord] != g2[coord]:
                return False
        return True

class Vector2: # ints only!
    def __init__(self, x=None, y=None):
        if y is None and x is not None:
            other = x
            self.x = other.x
            self.y = other.y
        elif x is None and y is None:
            self.x = 0
            self.y = 0
        elif x is not None and y is not None:
            self.x = x
            self.y = y
        else:
            assert False

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)

    @property
    def w(self): return self.x

    @property
    def h(self): return self.y

    def cw(self, amt=1):
        val = self
        for _ in range(0, amt):
            val = Vector2(-val.y, val.x)
        return val

    def ccw(self, amt=1):
        val = self
        for _ in range(0, amt):
            val = Vector2(val.y, -val.x)
        return val

    def __repr__(self):
        return '<{}, {}>'.format(self.x, self.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __div__(self, other):
        if isinstance(other, Vector2):
            return Vector2(int(self.x / other.x), int(self.y / other.y))
        else:
            return Vector2(int(self.x / other), int(self.y / other))

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

V = Vector2
