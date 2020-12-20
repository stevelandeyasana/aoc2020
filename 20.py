#!/usr/bin/env python

from util import *

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

    def __setitem__(self, k, val):
        assert isinstance(k, Vector2)
        self.cells[k] = val

    def copy(self):
        return Grid(size=self.size, cells={k: v for k, v in self.cells.items()})

    @property
    def w(self): return self.size.x
    @property
    def h(self): return self.size.y

    @property
    def coords(self):
        for y in range(0, self.size.y):
            for x in range(0, self.size.x):
                yield V(x, y)

    def neighbor(self, coord, delta):
        return self.cells.get(coord + delta, None)

    @property
    def top_row(self):
        return self._row(V(0, 0), V(1, 0))

    @property
    def top2_row(self):
        return self._row(V(self.w - 1, 0), V(-1, 0))

    @property
    def bottom_row(self):
        return self._row(V(self.w - 1, self.h - 1), V(-1, 0))

    @property
    def bottom2_row(self):
        return self._row(V(0, self.h - 1), V(1, 0))

    @property
    def left_row(self):
        return self._row(V(0, self.h - 1), V(0, -1))

    @property
    def left2_row(self):
        return self._row(V(0, 0), V(0, 1))

    @property
    def right_row(self):
        return self._row(V(self.w - 1, 0), V(0, 1))

    @property
    def right2_row(self):
        return self._row(V(self.w - 1, self.h - 1), V(0, -1))

    @property
    def all_sides(self):
        return [self.top_row, self.right_row, self.bottom_row, self.left_row]

    def _row(self, start, delta):
        return ''.join(list(self.__row(start, delta)))

    def __row(self, start, delta):
        pos = start
        while pos.x < self.w and pos.y < self.h and pos.x >= 0 and pos.y >= 0:
            yield self[pos]
            pos += delta

    def print(self):
        for y in range(0, self.size.y):
            print(''.join([self[V(x, y)] for x in range(0, self.size.x)]))
        print()

    def __repr__(self):
        return '\n' + '\n'.join([
            ''.join([self[V(x, y)] for x in range(0, self.size.x)])
            for y in range(0, self.size.y)])

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

    def min(self, other):
        return Vector2(min(self.x, other.x), min(self.y, other.y))

    def max(self, other):
        return Vector2(max(self.x, other.x), max(self.y, other.y))

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

PART = "a"


@attr.s
class Tile:
    id = attr.ib()
    grid = attr.ib()

    n = attr.ib(default=set)
    n2 = attr.ib(default=set)
    e = attr.ib(default=set)
    e2 = attr.ib(default=set)
    s = attr.ib(default=set)
    s2 = attr.ib(default=set)
    w = attr.ib(default=set)
    w2 = attr.ib(default=set)

    @property
    def is_northwest(self):
        if self.n or self.n2 or self.w or self.w2:
            return False
        return True

    def rotate_cw(self):
        n = self.w
        n2 = self.w2
        e = self.n
        e2 = self.n2
        s = self.e
        s2 = self.e2
        w = self.s
        w2 = self.s2
        self.n = n
        self.n2 = n2
        self.e = e
        self.e2 = e2
        self.s = s
        self.s2 = s2
        self.w = w
        self.w2 = w2

    @property
    def num_filled_edges(self):
        num = 0
        if self.n or self.n2:
            num += 1
        if self.s or self.s2:
            num += 1
        if self.e or self.e2:
            num += 1
        if self.w or self.w2:
            num += 1
        return num

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

class Supergrid:
    def __init__(self, tiles):
        self.tiles = {t.id: t for t in tiles}
        # print(self.tiles)
        self.candidates = collections.defaultdict(set)
        self._add_candidates()

        for t in self.tiles.values():
            t.n = self.candidates[t.grid.top_row] - set([t.id])
            t.e = self.candidates[t.grid.right_row] - set([t.id])
            t.s = self.candidates[t.grid.bottom_row] - set([t.id])
            t.w = self.candidates[t.grid.left_row] - set([t.id])
            t.n2 = self.candidates[t.grid.top2_row] - set([t.id])
            t.e2 = self.candidates[t.grid.right2_row] - set([t.id])
            t.s2 = self.candidates[t.grid.bottom2_row] - set([t.id])
            t.w2 = self.candidates[t.grid.left2_row] - set([t.id])
            # print(t)
        print(len(self.tiles))

        assert 1021 in self.tiles[2053].n
        corners = [t.id for t in self.tiles.values() if t.num_filled_edges == 2]
        print(corners)

        self.multiplied_corners = 1
        for c in corners:
            self.multiplied_corners *= c

        print(self.tiles[corners[0]])

        self.nw = self.tiles[corners[0]]
        while not self.nw.is_northwest:
            self.nw.rotate_cw()
        print(self.nw)

    def _add_candidates(self):
        for t in self.tiles.values():
            for side in t.grid.all_sides:
                self.candidates[side].add(t.id)


id_re = re.compile(r'Tile (\d+):')
def run():
    sg = Supergrid(tiles=[
        Tile(id=int(id_re.match(g[0]).group(1)), grid=Grid(lines=g[1:]))
        for g in read_multiline_groups()])
    return sg.multiplied_corners

answer = run()

PART = "b"

sys.exit(0)


print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=20, year=2020)
