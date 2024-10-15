from timeit import timeit
timeit('"-".join([str(n) for n in range(i)])',
       number=10000, setup="i = 10000")
