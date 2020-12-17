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

class Vector3: # ints only!
    def __init__(self, x=None, y=None, z=None):
        if y is None and x is not None:
            other = x
            self.x = other.x
            self.y = other.y
            self.z = other.z
        elif x is None and y is None and z is None:
            self.x = 0
            self.y = 0
            self.z = 0
        elif x is not None and y is not None and z is not None:
            self.x = x
            self.y = y
            self.z = z
        else:
            assert False

    def __repr__(self):
        return '<{}, {}, {}>'.format(self.x, self.y, self.z)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vector3(self.x * other, self.y * other, self.z * other)

    def __div__(self, other):
        if isinstance(other, Vector2):
            return Vector3(int(self.x / other.x), int(self.y / other.y), int(self.z / other.z))
        else:
            return Vector3(int(self.x / other), int(self.y / other), int(self.z / other))

    def __eq__(self, other):
        if isinstance(other, Vector3):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            return False
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))

    @property
    def neighbors(self):
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                for z in (-1, 0, 1):
                    if x == 0 and y == 0 and z == 0:
                        continue
                    yield V3(self.x + x, self.y + y, self.z + z)

V3 = Vector3


class Grid3:
    def __init__(self, lines=None, size=None, cells=None):
        self.cells = {}
        self.size = V3()
        self.size.z = 1
        self.min = V3()
        self.max = V3()
        if lines is not None:
            for line in lines:
                line = line.rstrip()
                self.size.x = len(line)
                for x in range(0, len(line)):
                    self.cells[V3(x, self.size.y, 0)] = line[x]
                self.size.y += 1
        if size is not None:
            self.size = size
        if cells is not None:
            self.cells = cells
        for k in self.cells.keys():
            self.min.x = min(self.min.x, k.x)
            self.max.x = max(self.max.x, k.x)
            self.max.y = min(self.max.y, k.y)
            self.max.y = max(self.max.y, k.y)
            self.max.z = min(self.max.z, k.z)
            self.max.z = max(self.max.z, k.z)

    def __getitem__(self, k):
        assert isinstance(k, Vector3)
        return self.cells.get(k, None)

    def get(self, x, y, z):
        return self[V3(x, y, z)]

    def __setitem__(self, k, val):
        assert isinstance(k, Vector3)
        self.min.x = min(self.min.x, k.x)
        self.max.x = max(self.max.x, k.x)
        self.min.y = min(self.min.y, k.y)
        self.max.y = max(self.max.y, k.y)
        self.min.z = min(self.min.z, k.z)
        self.max.z = max(self.max.z, k.z)

        self.cells[k] = val
    
    def set(self, x, y, z, val):
        self.cells[V(x, y, z)] = val

    def copy(self):
        g2 = Grid3(size=self.size, cells={k: v for k, v in self.cells.items()})
        g2.min = self.min
        g2.max = self.max
        return g2

    @property
    def coords(self):
        return self.cells.keys()
        # for y in range(0, self.size.y):
        #     for x in range(0, self.size.x):
        #         yield V(x, y)

    def neighbor(self, coord, delta):
        return self.cells.get(coord + delta, None)

    def print(self):
        for z in range(self.min.z, self.max.z + 1):
            print("z={}:", z)
            for y in range(self.min.y, self.max.y + 1):
                print(''.join([self[V3(x, y, z)] or '_' for x in range(self.min.x, self.max.x + 1)]))
            print()

    def __eq__(self, g2):
        if self.size != g2.size:
            return False
        for coord in self.coords:
            if self[coord] != g2[coord]:
                return False
        return True