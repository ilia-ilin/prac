from collections import defaultdict



class Omnibus:
    cnt = defaultdict(int)
    def __init__(self):
        self.__params__ = defaultdict(lambda: False)
        
    def __setattr__(self, name, value):
        if name[0] == "_":
            self.__dict__[name] = value
        else:
            if not self.__params__[name]:
                self.__params__[name] = True
                Omnibus.cnt[name] += 1
        
    def __getattr__(self, name):
        if name[0] == "_":
            return self.__dict__[name]
        return Omnibus.cnt[name]
    
    def __delattr__(self, name):
        if name[0] == "_":
            del self.__dict__[name]
        else:
            if self.__params__[name]:
                self.__params__[name] = False
                Omnibus.cnt[name] -= 1

import sys
exec(sys.stdin.read())
