matr1 = [eval(input())]
n = 1 if type(matr1[0]) == int else len(matr1[0])
if n == 1:
    print(matr1[0] * eval(input()))
else:
    for _ in range(1, n):
        matr1.append(eval(input()))
    matr2 = [[elm] for elm in eval(input())]
    for _ in range(1, n):
        for i, elm in enumerate(eval(input())):
            matr2[i].append(elm)
    matr3 = []
    for i in range(0, n):
        matr3.append([])
        for j in range(0, n):
            matr3[i].append(sum([matr1[i][k] * matr2[j][k] for k in range(0, n)]))
    for row in matr3:
        print(*row, sep = ',')
