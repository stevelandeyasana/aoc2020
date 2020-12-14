#!/usr/bin/env python

from util import *

PART = "a"

MASK_RE = re.compile(r'^mask = ([X01]+)$')
MEM_RE = re.compile(r'^mem\[(\d+)] = (\d+)$')

Inst = collections.namedtuple('Inst', ('addr', 'val', 'kind'))

program = []
for line in read_data():
    m1 = MASK_RE.match(line.strip())
    m2 = MEM_RE.match(line.strip())
    if m1:
        program.append(Inst(None, m1.group(1), 'mask'))
    elif m2:
        program.append(Inst(int(m2.group(1)), int(m2.group(2)), 'mem'))
    else:
        print(line)
        assert False

class ProgramState_part1:
    def __init__(self, program):
        self.program = program
        self.mask = 'X' * 36
        self.ormask = 0
        self.offmask = pow(2, 36) - 1
        self.memory = {}

    def run(self):
        for inst in self.program:
            if inst.kind == 'mask':
                self.mask = inst.val
                self.ormask = 0
                self.offmask = pow(2, 36) - 1
                for i, char in enumerate(reversed(self.mask)):
                    if char == 'X':
                        pass
                    elif char == '1':
                        self.ormask |= 1 << i
                    elif char == '0':
                        self.offmask &= pow(2, 36) - 1 - (1 << i)
            elif inst.kind == 'mem':
                self.update_memory(inst)
            else:
                assert False
        return sum(self.memory.values())

    def update_memory(self, inst):
        val = (inst.val | self.ormask) & self.offmask
        self.memory[inst.addr] = val
        print(inst.addr, "->", val)


PART = "b"

class ProgramState:
    def __init__(self, program):
        self.program = program
        self.mask = 'X' * 36
        self.ormask = 0
        self.floating_bits = []
        self.addr_cache = [] # unused
        self.memory = {}

    def run(self):
        for inst in self.program:
            if inst.kind == 'mask':
                self.mask = inst.val
                self.ormask = 0
                self.addr_cache = []
                self.floating_bits = []
                for i, char in enumerate(reversed(self.mask)):
                    if char == 'X':
                        self.floating_bits.append(i)
                    elif char == '1':
                        self.ormask |= 1 << i
                # print(self.floating_bits)
            elif inst.kind == 'mem':
                # print(bin(inst.addr))
                self.update_memory(inst)
            else:
                assert False
        return sum(self.memory.values())

    def update_memory(self, inst):
        addr = inst.addr | self.ormask

        for subaddr in self.get_subaddrs(addr, 0):
            # print(subaddr, "/", bin(subaddr), "->", inst.val)
            self.memory[subaddr] = inst.val

    def get_subaddrs(self, addr, start_i):
        if start_i >= len(self.floating_bits):
            yield addr
            return

        for subvalue in self.get_subaddrs(addr, start_i + 1):
            on = 1 << self.floating_bits[start_i]
            off = pow(2, 36) - 1 - (1 << self.floating_bits[start_i])
            yield subvalue & off
            yield subvalue | on


answer = ProgramState(program).run()

# print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=14, year=2020)
