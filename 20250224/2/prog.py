#MUD
import sys
import cowsay


#mesh[y][x]
#point(x, y)
mesh = [(10 * [None]) for _ in range(10)]

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class entity:
    def __init__(self, name, msg):
        self.name = name
        self.msg = msg

def debug_print():
    for line in mesh:
        for elm in line:
            print(elm, end='\t')
        print()
    print()

def move_player(pos, vec):
    newpos = point((pos.x + vec.x + 10) % 10, (pos.y + vec.y + 10) % 10)
    
    print(f'Moved to ({newpos.x}, {newpos.y})') 
    if mesh[newpos.y][newpos.x]:
        encounter(newpos)
    
    return newpos

def add_monster(name, pos, msg):
    if name not in cowsay.list_cows():
        print('Cannot add unknown monster')
        return
    print(f'Added monster {name} to ({pos.x}, {pos.y}) saying {msg}')
    if mesh[pos.y][pos.x]:
        print('Replaced the old monster')
    mesh[pos.y][pos.x] = entity(name, msg)

def encounter(pos):
    print(cowsay.cowsay(mesh[pos.y][pos.x].msg, cow=mesh[pos.y][pos.x].name))

def main():
    playerPos = point(0, 0)
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split()
        cmd = parts[0]
        
        try:
            if cmd == "up":
                playerPos = move_player(playerPos, point(0, -1))
            elif cmd == "down":
                playerPos = move_player(playerPos, point(0, 1))
            elif cmd == "left":
                playerPos = move_player(playerPos, point(-1, 0))
            elif cmd == "right":
                playerPos = move_player(playerPos, point(1, 0))
            elif cmd == "addmon":
                if len(parts) != 5:
                    raise ValueError
                name = parts[1]
                x = int(parts[2])
                y = int(parts[3])
                hello = parts[4]
                add_monster(name, point(x, y), hello)
            else:
                print('Invalid command')
        except:
            print('Invalid arguments')

if __name__ == "__main__":
    main()