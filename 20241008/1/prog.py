from fractions import Fraction

s, w, *tail = input().split(", ")
na = int(tail[0])
nb = int(tail[na + 2])
s = Fraction(s)
w = Fraction(w)

pa = Fraction(0)
t = Fraction(1)
for i in tail[na + 1:0:-1]:
    pa += t * Fraction(i)
    t *= s

pb = Fraction(0)
t = Fraction(1)
for i in tail[-1:-nb - 2:-1]: 
    pb += t * Fraction(i)
    t *= s
pb *= w
print(pa == pb)

# 1, -1/8, 2, 1, -5/2, 1, 1, 1, 3