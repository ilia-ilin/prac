def smul(n):
    num = n
    summ = 0
    while num > 0:
        summ += num % 10;
        num //= 10
    return (":=)" if summ == 6 else n)

N = int(input())
a, b, c = smul(N * N), smul(N * (N + 1)), smul(N * (N + 2))
print(N, " * ", N, " = ", a, " ", N, " * ", N + 1, " = ", b, " ", N, " * ", N + 2, " = ", c, sep = '')
a, b, c = smul((N + 1) * N), smul((N + 1) * (N + 1)), smul((N + 1) * (N + 2))
print(N + 1, " * ", N, " = ", a, " ", N + 1, " * ", N + 1, " = ", b, " ", N + 1, " * ", N + 2, " = ", c, sep = '')
a, b, c = smul((N + 2) * N), smul((N + 2) * (N + 1)), smul((N + 2) * (N + 2))
print(N + 2, " * ", N, " = ", a, " ", N + 2, " * ", N + 1, " = ", b, " ", N + 2, " * ", N + 2, " = ", c, sep = '')
