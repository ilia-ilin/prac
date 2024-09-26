lst = eval(input())
if type(lst) == int:
    print([lst])
else:
    lst = list(lst)
    for i in range(1, len(lst)):
        for j in range(0, len(lst) - i):
            if (lst[j] * lst[j]) % 100 > (lst[j + 1] * lst[j + 1]) % 100:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    print(lst)
