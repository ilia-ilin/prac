a, b, c = eval(input())
print(max(a,b,c) < sum((a,b,c)) - max(a,b,c) and min(a, b, c) > 0 )
