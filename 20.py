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
    
    def cull(self, vals):
        return
        self.n -= vals
        self.n2 -= vals
        self.s -= vals
        self.s2 -= vals
        self.e -= vals
        self.e2 -= vals
        self.w -= vals
        self.w2 -= vals

    @property
    def is_northwest(self):
        if self.n or self.n2 or self.w or self.w2:
            return False
        return True

    def rotate_cw(self):
        g2 = Grid(size=self.grid.size)
        for x in range(self.grid.w):
            for y in range(self.grid.h):
                g2[V(self.grid.w - 1 - y, x)] = self.grid[V(x, y)]
        self.grid = g2

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

    def flip_horizontal(self):
        g2 = Grid(size=self.grid.size)
        for y in range(0, self.grid.h):
            for x in range(0, self.grid.w):
                g2[V(self.grid.w - 1 - x, y)] = self.grid[V(x, y)]
        w = self.e2
        w2 = self.e
        e = self.w2
        e2 = self.w
        self.w = w
        self.w2 = w2
        self.e = e
        self.e2 = e2
        self.grid = g2

    def flip_vertical(self):
        g2 = Grid(size=self.grid.size)
        for y in range(0, self.grid.h):
            for x in range(0, self.grid.w):
                g2[V(x, self.grid.h - 1 - y)] = self.grid[V(x, y)]
        s = self.n2
        s2 = self.n
        n = self.s2
        n2 = self.s
        self.s = s
        self.s2 = s2
        self.n = n
        self.n2 = n2
        self.grid = g2

    # turn e2 into e by flipping and rotating it
    def shift_e(self, tiles):
        t_id = self.e2.pop() if self.e2 else self.e.pop()
        self.e.add(t_id) # let's be optimistic
        t = tiles[t_id]

        for i in range(4):
            if t.grid.left2_row == self.grid.right_row:
                return t
            elif t.grid.left_row == self.grid.right_row:
                t.flip_vertical()
                return t
            else:
                t.rotate_cw()

        print(self)
        print(t)
        assert False

        return t

    # turn e2 into e by flipping and rotating it
    def shift_s(self, tiles):
        t_id = self.s2.pop() if self.s2 else self.s.pop()
        self.e.add(t_id) # let's be optimistic
        t = tiles[t_id]

        for i in range(4):
            # if self.grid.bottom_row == t.grid.bottom_row:
            #     t.flip_vertical()
            #     assert t.e or t.e2
            #     return t
            if self.grid.bottom2_row == t.grid.top_row:
                if not (t.e or t.e2):
                    t.flip_horizontal()
                assert t.e or t.e2
                return t
            elif self.grid.bottom_row == t.grid.top_row:
                t.flip_horizontal()
                if not (t.e or t.e2):
                    t.flip_horizontal()
                return t
            else:
                t.rotate_cw()

        print(self)
        print(t)
        assert False

        return t

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
        # print(len(self.tiles))

        assert 1021 in self.tiles[2053].n
        corners = [t.id for t in self.tiles.values() if t.num_filled_edges == 2]
        # print(corners)

        self.multiplied_corners = 1
        for c in corners:
            self.multiplied_corners *= c

        # print(self.tiles[corners[0]])

        self.nw = self.tiles[corners[0]]
        while not self.nw.is_northwest:
            self.nw.rotate_cw()
        print(self.nw)

        already_matched = set()

        self.result = [[self.nw]]
        t_last = self.nw
        match_dir = 'e'
        while True:
            t_last.cull(already_matched)
            already_matched.add(t_last.id)
            if match_dir == 'e':
                # print(len(self.result[-1]), ",", len(self.result), "E:", t_last.id, t_last.e, t_last.e2)
                try:
                    assert len(t_last.e) + len(t_last.e2) == 1
                except AssertionError as e:
                    print(self.result[-2][0])
                    print(t_last)
                    raise e
                t_last = t_last.shift_e(self.tiles)
                self.result[-1].append(t_last)
                if not t_last.e and not t_last.e2:
                    match_dir = 's'
                    # print("row", len(self.result), ":", [t.id for t in self.result[-1]])
                    # typewriter back to beginning
                    t_last = self.result[-1][0]
                    self.result.append([])
            elif match_dir == 's':
                # print(len(self.result[-1]), ",", len(self.result), "S:", t_last.id, t_last.s, t_last.s2)
                try:
                    assert len(t_last.s) + len(t_last.s2) == 1
                except AssertionError:
                    break
                match_dir = 'e'
                t_last = t_last.shift_s(self.tiles)
                self.result[-1].append(t_last)

        self.result.remove(self.result[-1])
        print(len(self.result[0]), len(self.result))

        self.char_grid = []
        for tile_y in range(len(self.result)):
            for y in range(0 if tile_y == 0 else 1, self.result[0][0].grid.h):
                chars = []
                for i, tile in enumerate(self.result[tile_y]):
                    for x in range(0 if i == 0 else 1, tile.grid.w):
                        chars.append(tile.grid[V(x, y)])
                self.char_grid.append(''.join(chars))
                self.char_grid.append('')

        print('\n'.join(self.char_grid).replace('\n\n', '\n'))
        with open('20grid.txt', 'w') as f:
            f.write("\n".join(self.char_grid).replace('\n\n', '\n'))

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
