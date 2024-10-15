sogl = set("bcdfghjklmnpqrstvwxz")
glas = set("aeiouy")
s = set(input())
print(len(s & glas), len(s & sogl))
