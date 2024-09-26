from random import sample

for i in range(0, 200):
    print(*sample(range(-100,101), 100), sep = ',')
