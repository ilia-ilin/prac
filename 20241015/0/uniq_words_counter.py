from collections import Counter
from timeit import Timer
def func(s):
    Counter(s.split())
s = '123 123 123'
print(Timer('func(s)', globals = globals()).autorange())
