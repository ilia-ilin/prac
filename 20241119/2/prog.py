class Num:
    def __get__(self, obj, cls):
        if "_num" not in dir(obj):
            obj._num = 0
        return obj._num
    def __set__(self, obj, val):
        if "real" in dir(val):
            obj._num = val
        elif "__len__" in dir(val):
            obj._num = len(val)

import sys
exec(sys.stdin.read())