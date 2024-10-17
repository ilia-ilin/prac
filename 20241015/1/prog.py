s = input().lower()
print(len({(s[i - 1], s[i]) for i in range(1, len(s)) if s[i - 1].isalpha() and s[i].isalpha()}))

#аwба%Ба б7