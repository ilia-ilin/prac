from itertools import islice, count
def slide(seq, n):
    for i in range(len(seq)):
        yield from islice(seq, i, i + n)


import sys
exec(sys.stdin.read())
