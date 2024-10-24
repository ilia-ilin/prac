from itertools import islice

def _fib():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def fib(m, n):
    yield from islice(_fib(), m, m + n)

import sys
exec(sys.stdin.read())
