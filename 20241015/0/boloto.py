from collections import Counter
text = Counter(input().split())
lst = Counter(input().split())
print(len(lst - text) == 0)
