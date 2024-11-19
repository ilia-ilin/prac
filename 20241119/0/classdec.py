class istype:
    def __init__(self, typ):
        self.typ = typ
    def __call__(self, f):
        def newfun(*args):
            for arg in args:
                if not isinstance(arg, self.typ):
                    raise TypeError
            return f(*args)
        return newfun

@istype(int)
def a(a, b, c):
    print(a, b, c)

@istype(str)
def b(a, b, c):
    print(a, b, c)
