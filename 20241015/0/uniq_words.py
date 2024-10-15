d = dict()
for word in input().split():
    if word in d:
        d[word] += 1
    else:
        d[word] = 1
print(d.items())
