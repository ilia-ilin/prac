def rbin(n, l = [1]):
    if(n == 1):
        print(*l, sep = '')
        return
    rbin(n - 1, l + [0])
    rbin(n - 1, l + [1])
