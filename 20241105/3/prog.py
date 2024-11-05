class Maze:
    def __init__(self, N):
        self.N = N
        self.maze = [["█"] * (2 * N + 1) for _ in range(2 * N + 1)]
        for i in range(N):
            for j in range(N):
                self.maze[2 * i + 1][2 * j + 1] = "·"
    def __setitem__(self, idx):
        return type(idx)
    def __str__(self):
        return "\n".join(["".join(s) for s in self.maze])
