def F():
    def fun():
        return x
    print(">", fun.__closure__[0])
    x = 3
    print(">", fun.__closure__[0].cell_contents)
    return fun

res = F()
print(res())
