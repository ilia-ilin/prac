#MUD
import sys
import cowsay

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class entity:
    def __init__(self, name, msg):
        self.name = name
        self.msg = msg

#mesh[y][x]
#point(x, y)
mesh = [(10 * [None]) for _ in range(10)]
playerPos = point(0, 0)

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

def shlex(line):
    if ' ' in line:
        cmd, params = line.split(' ', 1)
    else:
        cmd = line
    global playerPos
    
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
            name, params = params.split(' ', 1)
            for _ in range(2):
                param, params = params.split(' ', 1)
                if param == "hello":
                    if ' ' in params:
                        paramval, params = params.split(' ', 1)
                    else:
                        paramval = params
                        params = ''
                    if paramval[0] == '"':
                        while paramval[-1] != '"':
                            if ' ' in params:
                                tmpval, params = params.split(' ', 1)
                                paramval += ' ' + tmpval
                            elif params[-1] == '"':
                                paramval += ' ' + params
                            else:
                                raise ValueError
                        paramval = paramval[1:-1]
                    hello = paramval
                # elif param == "hp":
                #     hp, params = params.split(' ', 1)
                #     hp = int(hp)
                elif param == "coords":
                    x, y, params = params.split(' ', 2)
                    pos = point(int(x), int(y))

            add_monster(name, pos, hello)
        else:
            print('Invalid command')
    except:
        print('Invalid arguments')

def main():
    print('<<< Welcome to Python-MUD 0.1 >>>')
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        shlex(line)

if __name__ == "__main__":
    main()