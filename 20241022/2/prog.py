from itertools import islice, count
def slide(seq, n):
    for i in count():
        print(slc := islice(seq, i, i + n))
        yield from slc
