import sys

chars = []
for line in sys.stdin:
    chars.append(line.strip('\n'))

import collections
chars2 = []
for x, line in enumerate(chars):
    for y, char in enumerate(line):
        if len(chars2) <= y:
            chars2.append([])
        chars2[y].append(char)
for line in chars2:
    print(''.join(line))