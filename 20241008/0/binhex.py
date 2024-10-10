def binhex(a, b):
    bmax = len(bin(b))
    xmax = len(hex(b))
    for i in range(a, b):
        print(f"{bin(i):>{bmax}} = {hex(i):>{xmax}}")
