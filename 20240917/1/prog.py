num = int(input())
s = "A "
if num % 25 == 0:
    if num % 2 == 0:
        s += "+ B - "
    else:
        s += "- B + "
else:
    s += "- B - "
if num % 8 == 0:
    s += "C +"
else:
    s += "C -"
print(s)
