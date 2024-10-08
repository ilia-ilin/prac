from math import sin
W, H = 60, 25
screen = [[" "] * W for i in range(H)]
def show(screen):
    print("\n".join("".join(s) for s in screen))
def scale(x, a, b, A, B):
    return (x - a) * (B - A) / (b - a) + A
def draw(fun, a, b, miny, maxy):
    for ix in range(W):
        x = scale(ix, 0, W - 1, a, b)
        iy = round(scale(sin(x), miny, maxy, 0, H - 1))
        screen[H - iy - 1][ix] = "*"
