from itertools import cycle


class Doubleton(type):
    _objs = None
    def __call__(cls, *args, **kw):
        if cls._objs is None:
            cls._objs = [super().__call__(*args, **kw)]
            return cls._objs[0]
        elif type(cls._objs) is list:
            obj = super().__call__(*args, **kw)
            cls._objs.append(obj)
            cls._objs = cycle(cls._objs)
            return obj
        else:
            return next(cls._objs)
