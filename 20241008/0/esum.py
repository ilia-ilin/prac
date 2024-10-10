from decimal import Decimal
def esum(N, one):
    s = one
    frac = one
    for n in range(1, N):
        frac *= n
        s += one / frac
    return s
