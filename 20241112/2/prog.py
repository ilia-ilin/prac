
class InvalidInput(Exception): pass
class BadTriangle(Exception): pass

def triangleSquare(inStr):
    try:
        (x1, y1), (x2, y2), (x3, y3) = eval(inStr)
    except:
        raise InvalidInput
    try:
        s = abs((x1 - x3) * (y2 - y3) - (y1 - y3) * (x2 - x3))
    except:
        raise BadTriangle
    if round(s, 2) == 0:
        raise BadTriangle
    return s / 2
while True:
    try:
        s = triangleSquare(input())
    except InvalidInput:
        print("Invalid input")
    except BadTriangle:
        print("Not a triangle")
    else:
        print(f"{s:.2f}")
        break

