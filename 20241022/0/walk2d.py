def walk2d():
    x, y = 0, 0
    while True:
        dx, dy = yield (x, y)
        x += dx
        y += dy
