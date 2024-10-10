from fractions import Fraction
from math import ceil

w = len(input()) - 2
gas, liquid = 0, 0

while (s := input())[1] == '.':
    gas += 1
while s[1] == '~':
    liquid += 1
    s = input()

h = gas + liquid  
gas *= w
liquid *= w
lnum = max(len(str(gas)), len(str(liquid)))

print("#" * (h + 2))
for i in range(gas // h):
    print("#", "." * h, "#",sep="")
for i in range(ceil(liquid / h)):
    print("#", "~" * h, "#",sep="")
print("#" * (h + 2))
print(f"{"." * round(20 * gas / max(gas, liquid)):<20} {gas:>{lnum}}/{gas + liquid}")
print(f"{"~" * round(20 * liquid / max(gas, liquid)):<20} {liquid:>{lnum}}/{gas + liquid}")

########
#......#
#~~~~~~#
#~~~~~~#
########

#####
#...#
#~~~#
#~~~#
#~~~#
#~~~#
#~~~#
#####