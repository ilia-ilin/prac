def minf(*funs):
    return lambda x: min(fun(x) for fun in funs)
