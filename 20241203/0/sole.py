class sole(type):
    def __new__(metacls, name, parents, namespace):
        if len(parents) > 1:
            raise TypeError(f"Cannot have more tan one parent")
        return super().__new__(metacls, name, parents, namespace)
