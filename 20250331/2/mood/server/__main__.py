# MUD-server
import asyncio
import cowsay
from io import StringIO


# mesh[y][x]
# point(x, y)
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class entity:
    def __init__(self, name: str, hp: int, msg: str) -> None:
        self.name = name
        self.hp = hp
        self.msg = msg


class player:
    def __init__(self, queue: asyncio.Queue):
        self.coords = point(0, 0)
        self.queue = queue


mesh = [(10 * [None]) for _ in range(10)]
players = {}
customMonsters = {
    "jgsbat": cowsay.read_dot_cow(StringIO(r"""
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


def encounter(name, msg) -> str:
    if name in cowsay.list_cows():
        return cowsay.cowsay(msg, cow=name)
    else:
        return cowsay.cowsay(msg, cowfile=customMonsters[name])


def move_player(player: str, dx, dy):
    coords = players[player].coords
    coords = point((coords.x + dx + 10) % 10, (coords.y + dy + 10) % 10)
    players[player].coords = coords
    response = f'Moved to ({coords.x}, {coords.y})'

    if mesh[coords.y][coords.x]:
        response += '\n' + encounter(
            mesh[coords.y][coords.x].name,
            mesh[coords.y][coords.x].msg)
    return response


def addmon(player, name, x, y, hp, msg):
    response = f'Added monster {name} to ({x}, {y}) saying {msg}'
    response_all = f'{player}: added monster {name} saying {msg}'
    if mesh[y][x]:
        response += '\nReplaced the old monster'
        response_all += '\nReplaced the old monster'
    mesh[y][x] = entity(name, hp, msg)
    return (response, response_all)


def attack(player, name, damage):
    monster = mesh[players[player].coords.y][players[player].coords.x]
    response_all = None
    if not monster or monster.name != name:
        response = f'No {name} here'
    else:
        damage = min(damage, monster.hp)
        monster.hp -= damage
        response = f'Attacked {name},  damage {damage} hp'
        response_all = f'{player}: attacked {name},  damage {damage} hp'
        if monster.hp == 0:
            response += f'\n{name} died'
            response_all += f'\n{name} died'
            mesh[players[player].coords.y][players[player].coords.x] = None
        else:
            response += f'\n{name} now has {monster.hp}'
            response_all += f'\n{name} now has {monster.hp}'

    return (response, response_all)


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
            players[me] = player(asyncio.Queue())

        for p in players:
            if p != me:
                await players[p].queue.put(f'{me} connected.')

        send = asyncio.create_task(reader.readline())
        receive = asyncio.create_task(players[me].queue.get())

        while not reader.at_eof():
            done, pending = await asyncio.wait(
                [send, receive],
                return_when=asyncio.FIRST_COMPLETED)

            for q in done:
                if q is send:
                    send = asyncio.create_task(reader.readline())
                    data = q.result()
                    cmd = data.decode().strip().split(' ')
                    response_all = None
                    if not cmd:
                        continue
                    if cmd[0] == "move":
                        response = move_player(me, int(cmd[1]), int(cmd[2]))
                    elif cmd[0] == "addmon":
                        name, x, y, hp, *msg = cmd[1:]
                        response, response_all = addmon(
                            me,
                            name,
                            int(x),
                            int(y),
                            int(hp),
                            ' '.join(msg))
                    elif cmd[0] == "attack":
                        name, damage = cmd[1], int(cmd[2])
                        response, response_all = attack(me, name, damage)
                    elif cmd[0] == "sayall":
                        msg = ' '.join(cmd[1:])
                        response = None
                        response_all = f'{me}: {msg}'
                    if response:
                        writer.write(
                            (response.replace('\n', '\\n') + '\n').encode())
                    await writer.drain()
                    if response_all:
                        for p in players:
                            if p != me:
                                await players[p].queue.put(response_all)
                        response_all = None
                elif q is receive:
                    receive = asyncio.create_task(players[me].queue.get())
                    writer.write(
                        (q.result().replace('\n', '\\n') + '\n').encode())
                    await writer.drain()
    finally:
        for p in players:
            if p != me:
                await players[p].queue.put(f'{me} disconnected.')
        writer.write(('closed\n').encode())
        await writer.drain()
        writer.close()
        del players[me]


async def main():
    server = await asyncio.start_server(handle_client, 'localhost', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
