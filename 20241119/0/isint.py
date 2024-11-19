def isint(f):
    def newfun(*args):
        for arg in args:
            if not isinstance(arg, int):
                raise TypeError
        return f(*args)
    return newfun

@isint
def a(a, b, c):
    print(a, b, c)
