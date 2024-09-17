count = 0
i = 1
while (num := eval(input())) != 0:
    if num == i:
        count += 1
    i += 1
print(count)
