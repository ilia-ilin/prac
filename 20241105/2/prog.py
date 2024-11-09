def vec(a, b, c):
    return ((a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0]))
    
def sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    return 0

class Triangle:
    def __init__(self, a, b, c):
        self.a = list(a)
        self.b = list(b)
        self.c = list(c)
        
    def __abs__(self):
        s = abs(vec(self.a, self.b, self.c)) / 2
        return s if s else 0
    
    def __bool__(self):
        return abs(self) != 0

    def __lt__(self, other):
        return abs(self) < abs(other)
        
    def __contains__(self, other):
        if type(other) == Triangle:
            if abs(other) == 0:
                return True
            return other.a in self and other.b in self and other.c in self
        else:
            AOB = abs(vec(self.a, self.b, other))
            BOC = abs(vec(self.b, self.c, other))
            COA = abs(vec(self.c, self.a, other))
            return abs(self) == (AOB + BOC + COA) / 2
    
    def __and__(self, other):
       if abs(self) == 0 or abs(other) == 0:
           return False
       return self.a in other or self.b in other or self.c in other or other.a in self or other.b in self or other.c in self
       
import sys
exec(sys.stdin.read())