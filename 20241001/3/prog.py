from math import *
def Calc(s, t, u):
    def calc(z, x = eval("lambda x: " + s), y = eval("lambda x: " + t)):
        x = x(z)
        y = y(z)
        return eval(u)
    return calc
print(Calc(*eval(input()))(eval(input())))