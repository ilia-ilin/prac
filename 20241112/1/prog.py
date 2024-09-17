from collections import UserString as UStr

class DivStr(UStr):
    def __init__(self, str = ""):
        super().__init__(str)
     
    def floordiv(self, n):
        i = 0
        d = len(self) // n
        if d == 0:
            return
        while d * (i + 1) <= len(self):
            yield self.data[i * d : (i + 1) * d]
            i += 1
    def __floordiv__(self, n):
        return self.floordiv(n)
    
    def __mod__(self, n):
        return self.__class__(self.data[len(self)//n*n:])


import sys
exec(sys.stdin.read())