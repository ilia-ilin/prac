def istype(typ):
    def decorator(f):
        def newfun(*args):
            for arg in args:
                if not isinstance(arg, self.typ):
                    raise TypeError
            return f(*args)
        return newfun
    return decorator

@istype(int)
def a(a, b, c):
    print(a, b, c)

@istype(str)
def b(a, b, c):
    print(a, b, c)
