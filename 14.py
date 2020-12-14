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

class ProgramState:
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


answer = ProgramState(program).run()

print(answer)
if len(sys.argv) > 1:
    sys.exit(0)
from aocd import submit
submit(answer, part=PART, day=14, year=2020)
