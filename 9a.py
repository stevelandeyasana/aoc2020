#!/usr/bin/env python

from util import *

@attr.s
class Inst:
    line = attr.ib()
    arg = attr.ib()
    num = attr.ib(converter=lambda s: int(s))

    def flipcopy(self):
        return Inst(line=self.line, arg='jmp' if self.arg == 'nop' else 'nop', num=self.num)

INPUT_RE = re.compile(r'^(\w+) ([+-]\d+)$')

instructions = [Inst(i, *INPUT_RE.match(line).groups()) for i, line in enumerate(read_data())]

class ProgramState:
    def __init__(self, instructions):
        self.accum = 0
        self.ptr = 0
        self.executed = set()
        self.instructions = instructions

    def exec_one(self):
        if self.ptr in self.executed:
            raise ValueError("Loop")
        
        self.executed.add(self.ptr)

        inst = self.instructions[self.ptr]

        if inst.arg == 'acc':
            self.accum += inst.num
            self.ptr += 1
        elif inst.arg == 'jmp':
            self.ptr += inst.num
        elif inst.arg == 'nop':
            self.ptr += 1
        else:
            assert False

    def exec(self):
        while True:
            try:
                self.exec_one()
            except ValueError:
                return None
            if self.ptr == len(self.instructions):
                return self.accum


for i in range(0, len(instructions)):
    state = ProgramState([] + instructions)
    state.instructions[i] = instructions[i].flipcopy()
    x = state.exec()
    if x is not None:
        answer = x
        break

print(answer)
sys.exit(0)
from aocd import submit
submit(answer, part="a", day=10, year=2020)