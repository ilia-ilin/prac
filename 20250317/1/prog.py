#MUD-server
import asyncio

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

def move_player(dx, dy):
    global playerPos
    newpos = point((playerPos.x + dx + 10) % 10, (playerPos.y + dy + 10) % 10)
    playerPos = newpos
    response = f'{newpos.x} {newpos.y} '

    if mesh[newpos.y][newpos.x]:
        response += f'{mesh[newpos.y][newpos.x].name} {mesh[newpos.y][newpos.x].msg}'
    else:
        response += 'noencounter'
    
    return response

def addmon(name, x, y, hp, msg):
    if mesh[y][x]:
        response = 'replaced'
    else:
        response = 'nonreplaced'
    mesh[y][x] = entity(name, hp, msg)
    return response


def attack(name, damage):
    monster = mesh[playerPos.y][playerPos.x]
    if not monster or monster.name != name:
        response = 'nomonster'
    else:
        damage = min(damage, monster.hp)
        monster.hp -= damage
        response = f'{damage} {monster.hp}'
        if monster.hp == 0:
            mesh[playerPos.y][playerPos.x] = None

    return response

async def handle_client(reader, writer):
    while data := await reader.readline():
        cmd = data.decode().strip().split(' ')
        if not cmd:
            continue
        if cmd[0] == "move":
            response = move_player(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == "addmon":
            name, x, y, hp, *msg = cmd[1:]
            response = addmon(name, int(x), int(y), int(hp), ' '.join(msg))
        elif cmd[0] == "attack":
            name, damage = cmd[1], int(cmd[2])
            response = attack(name, damage)

        writer.write((response + '\n').encode())
        await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, 'localhost', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())