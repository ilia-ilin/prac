class annot:
    a: int
    def __init__(self, val):
        if type(val) == self.__annotations__["a"]:
            self.__class__.a = val
        else:
            raise TypeError(f"val is not {self.__annotations__['a']}")
