#MUD
import cmd
import sys
import cowsay
from io import StringIO

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class entity:
    def __init__(self, name: str, hp: int, msg: str) -> None:
        self.name = name
        self.hp = hp
        self.msg = msg

#mesh[y][x]
#point(x, y)
mesh = [(10 * [None]) for _ in range(10)]
playerPos = point(0, 0)
customMonsters = dict()

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

def add_monster(name, pos, hp, msg):
    if name not in cowsay.list_cows() and name not in customMonsters:
        print('Cannot add unknown monster')
        return
    print(f'Added monster {name} to ({pos.x}, {pos.y}) saying {msg}')
    if mesh[pos.y][pos.x]:
        print('Replaced the old monster')
    mesh[pos.y][pos.x] = entity(name, hp, msg)

def encounter(pos):
    if mesh[pos.y][pos.x].name in cowsay.list_cows():
        print(cowsay.cowsay(mesh[pos.y][pos.x].msg, cow=mesh[pos.y][pos.x].name))
    else:
        print(cowsay.cowsay(mesh[pos.y][pos.x].msg, cowfile=customMonsters[mesh[pos.y][pos.x].name]))


def add_custom():
    customMonsters["jgsbat"] = cowsay.read_dot_cow(StringIO(r"""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\\\--//|.'-._  (
     )'   .'\\/o\\/o\\/'.   `(
      ) .' . \\====/ . '. (
       )  / <<    >> \\  (
        '-._/``  ``\\_.-'
  jgs     __\\\\'--'//__
         (((""`  `"")))
EOC
"""))

class MUD(cmd.Cmd):
    intro = '<<< Welcome to Python-MUD 0.1 >>>'
    prompt = 'MUD>> '

    def do_up(self, arg):
        "Move up"
        global playerPos
        playerPos = move_player(playerPos, point(0, -1))

    def do_down(self, arg):
        "Move down"
        global playerPos
        playerPos = move_player(playerPos, point(0, 1))

    def do_left(self, arg):
        "Move left"
        global playerPos
        playerPos = move_player(playerPos, point(-1, 0))

    def do_right(self, arg):
        "Move right"
        global playerPos
        playerPos = move_player(playerPos, point(1, 0))

    def do_addmon(self, arg):
        """
        Add a monster.
        Syntax: addmon name hp <number> coords <x> <y> hello "Message"
        """
        try:
            tokens = arg.split()
            name = tokens[0]
            hp_idx = tokens.index("hp")
            coords_idx = tokens.index("coords")
            hello_idx = tokens.index("hello")
            hp = int(tokens[hp_idx + 1])
            x = int(tokens[coords_idx + 1])
            y = int(tokens[coords_idx + 2])
            
            idxs = sorted([hp_idx, coords_idx, hello_idx])
            idxs.append(None)
            lastidx = idxs[idxs.index(hello_idx) + 1]

            msg = ' '.join(tokens[hello_idx + 1:lastidx]).strip('"')
            add_monster(name, point(x, y), hp, msg)
        except Exception as e:
            print("Invalid arguments")

def main():
    add_custom()
    
    MUD().cmdloop()

    # for line in sys.stdin:
    #     line = line.strip()
    #     if not line:
    #         continue
        
    #     shlex(line)

if __name__ == "__main__":
    main()