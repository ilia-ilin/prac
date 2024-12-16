def objcount(cls):
    cls.counter = 0
    cls.___init___ = cls.__init__
    def __init__(self):
        cls.___init___(self)
        cls.counter += 1
    cls.__init__ = __init__

    cls.___del___ = cls.__del__
    def __del__(self):
        cls.___del___(self)
        cls.counter -= 1
    cls.__del__ = __del__
    return cls

@objcount
class C:
    def __init__(self):
        self.bbb = 1
    def __del__(self):
        pass

c, d, e = C(), C(), C()
print(C.counter)
c = 100500
print(C.counter)
print(d.bbb)

import sys
exec(sys.stdin.read())