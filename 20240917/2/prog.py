summ = 0
while summ <= 21 and (num := int(input())) > 0:
    summ += num
    if summ > 21:
        num = summ
else:
    print(num)
