class person:
    def __init__(self):
        self._age = None

    @property
    def age(self):
        if self._age == 42:
            print("secret value!")
            return -1
        return self._age

    @age.setter
    def age(self, val):
        if val > 128:
            print("too old!")
            raise ValueError
        self._age = val
