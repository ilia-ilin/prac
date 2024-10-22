from simple import gen
from itertools import *
print(list(islice(dropwhile(lambda x: x < 1.6, gen()), 10)))
