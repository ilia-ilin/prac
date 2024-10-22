def gen():
    i = 1
    s = 0
    while True:
        s += 1 / (i * i)
        yield s
        i += 1
