from queue import Queue

class Maze:
    def __init__(self, N):
        self.N = N
        self.colored = False

        self.maze = [["█"] * (2 * N + 1) for _ in range(2 * N + 1)]
        for i in range(N):
            for j in range(N):
                self.maze[2 * i + 1][2 * j + 1] = "·"
    
    def __setitem__(self, slc, val):
        self.colored = False
        x0, y0, y1 = slc
        y0, x1 = y0.start, y0.stop
        
        if x0 != x1 and y0 != y1:
            return
        elif x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
            for y in range(y0, y1):
                self.maze[2 * y + 2][2 * x0 + 1] = val
        else:
            if x0 > x1:
                x0, x1 = x1, x0
            for x in range(x0, x1):
                self.maze[2 * y0 + 1][2 * x + 2] = val        
    
    def __getitem__(self, slc):
        if not self.colored:
            self.__color__()
            self.colored = True
        x0, y0, y1 = slc
        y0, x1 = y0.start, y0.stop
        return self.colors[y0][x0] == self.colors[y1][x1]
    
    def __color__(self):
        self.colors = [[0] * self.N for _ in range(self.N)]
        color = 0
        for i in range(self.N):
            for j in range(self.N):
                if self.colors[i][j] == 0:
                    toadd = Queue()
                    color += 1
                    toadd.put((i, j))
                    while not toadd.empty():
                        y, x = toadd.get()
                        if x + 1 < self.N and self.colors[y][x + 1] == 0 and self.maze[2 * y + 1][2 * x + 2] == "·":
                            toadd.put((y, x + 1))
                        if y + 1 < self.N and self.colors[y + 1][x] == 0 and self.maze[2 * y + 2][2 * x + 1] == "·":
                            toadd.put((y + 1, x))
                        if x > 0 and self.colors[y][x - 1] == 0 and self.maze[2 * y + 1][2 * x] == "·":
                            toadd.put((y, x - 1))
                        if y > 0 and self.colors[y - 1][x] == 0 and self.maze[2 * y][2 * x + 1] == "·":
                            toadd.put((y - 1, x))
                        self.colors[y][x] = color
    
    def __str__(self):
        return "\n".join(["".join(s) for s in self.maze])

import sys
exec(sys.stdin.read())
