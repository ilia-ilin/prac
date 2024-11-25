class Vowel:
    __slots__ = list("aeiouy")
    
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
    
    @property
    def full(self):
        for attr in self.__slots__:
            if not hasattr(self, attr):
                return False
        return True
        
    @full.setter
    def full(self, val):
        pass
        
    @property
    def answer(self):
        return 42
    
    def __str__(self):
        s = []
        for attr in "aeiouy":
            if hasattr(self, attr):
                s.append(f"{attr}: {getattr(self, attr)}")
        return ", ".join(s)


import sys
exec(sys.stdin.read())