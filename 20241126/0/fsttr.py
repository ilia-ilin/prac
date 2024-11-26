from pathlib import Path

f = open("fsttr.py", "r")
lines = f.readlines()
i = 0
s = ""
while 3 * len(s) < len("".join(lines)):
    s += lines[i]
    i += 1

print(s)

#123
#123
#123
#123
#123
#123
#123
#123
#123
#123
#123
#123
#123