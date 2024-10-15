from timeit import Timer
def sg(s):
    sogl = set("bcdfghjklmnpqrstvwxz")
    glas = set("aeiouy")
    print(len(s & glas), len(s & sogl))

print(Timer("timeit(s)", setup='s = "qweqqqrty"').autorange())
