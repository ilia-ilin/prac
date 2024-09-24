matr = [eval(input())]
l = len(matr[0])
h = 1
lens = []
while (s := input()):
    s = eval(s)
    lens.append(len(s) == l)
    matr.append(s)
    h += 1
lens.append(h == l)
print(all(lens))
if(all(lens)):
    for i in range(0, len(matr[0])):
        for j in range(0, len(matr)):
            print(matr[j][i], end = ' ')
        print()
