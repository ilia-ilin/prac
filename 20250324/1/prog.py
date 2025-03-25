#MUD-server
import asyncio
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
players = {}
customMonsters = {
    "jgsbat" : cowsay.read_dot_cow(StringIO(r"""
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
}

def encounter(name, msg):
    if name in cowsay.list_cows():
        return cowsay.cowsay(msg, cow=name)
    else:
        return cowsay.cowsay(msg, cowfile=customMonsters[name])

def move_player(player, dx, dy):
    players[player] = point((players[player].x + dx + 10) % 10, (players[player].y + dy + 10) % 10)
    response = f'Moved to ({players[player].x}, {players[player].y})'

    if mesh[players[player].y][players[player].x]:
        response += f'\n{encounter(mesh[players[player].y][players[player].x].name, mesh[players[player].y][players[player].x].msg)}'
    
    return response

def addmon(name, x, y, hp, msg):
    response = f'Added monster {name} to ({x}, {y}) saying {msg}'
    if mesh[y][x]:
        response += 'Replaced the old monster'
    mesh[y][x] = entity(name, hp, msg)
    return response

def attack(player, name, damage):
    monster = mesh[players[player].y][players[player].x]
    if not monster or monster.name != name:
        response = f'No {name} here'
    else:
        damage = min(damage, monster.hp)
        monster.hp -= damage
        response = f'Attacked {name},  damage {damage} hp'
        if monster.hp == 0:
            response += f'\n{name} died'
            mesh[players[player].y][players[player].x] = None
        else:
            response += f'\n{name} now has {monster.hp}'

    return response

async def handle_client(reader, writer):
    try:
        me = await reader.readline()
        me = me.decode().strip()

        if me in players:
            writer.write(('error\n').encode())
            writer.close()
            return
        else:
            writer.write(('accept\n').encode())
            players[me] = point(0, 0)

        while data := await reader.readline():
            cmd = data.decode().strip().split(' ')
            if not cmd:
                continue
            if cmd[0] == "move":
                response = move_player(me, int(cmd[1]), int(cmd[2]))
            elif cmd[0] == "addmon":
                name, x, y, hp, *msg = cmd[1:]
                response = addmon(name, int(x), int(y), int(hp), ' '.join(msg))
            elif cmd[0] == "attack":
                name, damage = cmd[1], int(cmd[2])
                response = attack(me, name, damage)

            writer.write((response.replace('\n', '\\n') + '\n').encode())
            await writer.drain()
    finally:
        writer.write(('closed\n').encode())
        await writer.drain()
        writer.close()

async def main():
    server = await asyncio.start_server(handle_client, 'localhost', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())