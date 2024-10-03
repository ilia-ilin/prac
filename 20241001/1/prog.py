def dominate(a, b):
    return a[0] >= b[0] and a[1] >= b[1]
def not_less(a, b):
    return dominate(a,b) or not dominate(b, a)
def Pareto(*pairs):
    pairs = [(p, True) for p in pairs]
    while True:
        for i, pair in enumerate(pairs):
            if pair[1]:
                pairs[i] = (pair[0], False)
                pairs = [p for p in pairs if not_less(p[0], pair[0])]
                break
        else:
            break
    return tuple([p[0] for p in pairs])
print(Pareto(*eval(input())))