from collections import Counter
n = int(input())
c = Counter()

def arrsplit(words: list, sep: str) -> list:
    new_words = []
    for word in words:
        new_words += [subword for subword in word.split(sep) if subword]
    return new_words

def filter_words(words: list) -> list:
    new_words = []
    for word in words:
        split_words = [word]
        for sep in ("'-,.!?:" + '"'):
            split_words = arrsplit(split_words, sep)
        new_words += split_words
    return new_words

while (s := input()):
    c += Counter(w for w in filter_words(s.lower().split()) if len(w) == n)

m = max(c.values())
print(*sorted([w for w in c if c[w] == m]))