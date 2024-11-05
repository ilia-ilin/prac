class Rectangle:
    rectcnt = 0
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        Rectangle.rectcnt += 1
        self.__dict__[f"rect_{self.rectcnt}"] = self.rectcnt
        
    def __abs__(self):
        return abs((self.x2 - self.x1) * (self.y2 - self.y1))

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __eq__(self, other):
        return abs(self) == abs(other)

    def __mul__(self, other):
        return Rectangle(self.x1 * other, self.y1 * other, self.x2 * other, self.y2 * other)

    def __rmul__(self, other):
        return self * other

    def __getitem__(self, idx):
        return ((self.x1,self.y1), (self.x1,self.y2), (self.x2,self.y2), (self.x2,self.y1))[idx]

    def __bool__(self):
        return abs(self) > 0

    def __del__(self):
        Rectangle.rectcnt -= 1
        print("Deleted")
        pass

    def __str__(self):
        return f"({self.x1},{self.y1})({self.x1},{self.y2})({self.x2},{self.y2})({self.x2},{self.y1})"
