class dump(type):
    @staticmethod
    def _wrapper(fun):
        def newfun(*args, **kwargs):
            print(f"{fun.__name__}: {args[1:]}, {kwargs}")
            return fun(*args, **kwargs)
        return newfun
    
    def __new__(cls, name, parents, ns, **kwds):
        new_ns = {fun : (dump._wrapper(ns[fun]) if callable(ns[fun]) else ns[fun]) for fun in ns}
        return super().__new__(cls, name, parents, new_ns)

import sys
exec(sys.stdin.read())