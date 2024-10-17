from math import *

funcs = {}
n_str = 1
while (s := input().split(' '))[0] != "quit":
    n_str += 1
    if s[0][0] == ':':
        func = s[0][1:]
        *params, body = s[1:]
        funcs[func] = eval(f"lambda {' '.join(params)}: {body}")
    else:
        params = map(eval, s[1:])
        print(funcs[s[0]](*params))
print(' '.join(s[1:])[1:-1].format(len(funcs) + 1, n_str))