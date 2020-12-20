import sys

chars = []
for line in sys.stdin:
    chars.append(line.strip('\n'))
    print(''.join(reversed(list(line.strip('\n')))))