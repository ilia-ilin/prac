f = input()
a, b = eval(input())
print(eval(f, {"x":a, "y":b}))
print(eval(f, {"x":b, "y":a}))
