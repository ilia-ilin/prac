class inp:
    a, b, c = input().split()

while True:
    match input().split():
        case ([inp.a, *tail] as s) if "yes" in s:
            print("1")
        case [inp.b]:
            print("2")
        case [inp.c, *tail, inp.b]:
            print("3")
