"""
MUD-сервер для текстовой многопользовательской игры.

Сервер реализует следующую функциональность:
- Управление игровым полем 10x10 с телепортацией через границы
- Обработка перемещений игроков и взаимодействия с монстрами
- Сетевой интерфейс для подключения клиентов через TCP
- Периодическое перемещение монстров по полю
- Система чата между игроками
"""

# MUD-server
import asyncio
import cowsay
import random
from io import StringIO


class point:
    """Точка на двумерной игровой карте.
    
    Attributes:
        x (int): Горизонтальная координата (0-9)
        y (int): Вертикальная координата (0-9)
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        """Сравнение координат двух точек."""
        if isinstance(other, point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self) -> int:
        """Генерация хеша для использования в словарях."""
        return hash((self.x, self.y))


class entity:
    """Сущность монстра на игровом поле.
    
    Args:
        name (str): Уникальное имя монстра
        hp (int): Текущий уровень здоровья
        msg (str): Сообщение при встрече с игроком
    """
    def __init__(self, name: str, hp: int, msg: str) -> None:
        self.name = name
        self.hp = hp
        self.msg = msg


class player:
    """Представление игрока в системе.
    
    Args:
        queue (asyncio.Queue): Очередь для отправки сообщений игроку
    """
    def __init__(self, queue: asyncio.Queue) -> None:
        self.coords = point(0, 0)
        self.queue = queue


monsters = {}   # coords: entity
players = {}    # name: player
directions = {
    'up': point(0, -1),
    'down': point(0, 1),
    'left': point(-1, 0),
    'right': point(1, 0)
}
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


def add_mod_10(p1: point, p2: point) -> point:
    """Вычисляет новые координаты с циклическими границами.
    
    Args:
        p1: Исходная позиция
        p2: Смещение
        
    Returns:
        Новая позиция (координаты по модулю 10)
    """
    return point((p1.x + p2.x) % 10, (p1.y + p2.y) % 10)


def encounter(name: str, msg: str) -> str:
    """Генерирует сообщение при встрече с монстром.
    
    Args:
        name: Имя монстра из cowsay
        msg: Текст сообщения
        
    Returns:
        Отформатированная строка с ASCII-артом
        
    Raises:
        KeyError: Для неизвестных имен монстров
    """
    if name in cowsay.list_cows():
        return cowsay.cowsay(msg, cow=name)
    else:
        return cowsay.cowsay(msg, cowfile=customMonsters[name])


def move_player(player: str, dx: int, dy: int) -> str:
    """Обрабатывает перемещение игрока.
    
    Args:
        player: Имя игрока
        dx: Смещение по X
        dy: Смещение по Y
        
    Returns:
        Статус перемещения и встречи с монстром
        
    Raises:
        KeyError: При несуществующем имени игрока
    """
    coords = add_mod_10(players[player].coords, point(dx, dy))
    players[player].coords = coords
    response = f'Moved to ({coords.x}, {coords.y})'

    if coords in monsters:
        response += '\n' + encounter(
            monsters[coords].name,
            monsters[coords].msg)

    return response


def addmon(player: str, name: str, coords: point, hp: int, msg: str) -> tuple[str, str]:
    """Добавляет или заменяет монстра на карте.
    
    Args:
        player: Имя инициатора команды
        name: Тип монстра
        coords: Позиция размещения
        hp: Здоровье монстра
        msg: Сообщение при встрече
        
    Returns:
        tuple: (локальное сообщение, глобальное уведомление)
    """
    response = f'Added monster {name} to ({coords.x}, {coords.y}) saying {msg}'
    response_all = f'{player}: added monster {name} saying {msg}'

    if coords in monsters:
        response += '\nReplaced the old monster'
        response_all += '\nReplaced the old monster'
    monsters[coords] = entity(name, hp, msg)

    return (response, response_all)


def attack(player: str, name: str, damage: int) -> tuple[str, str | None]:
    """Обрабатывает атаку монстра.
    
    Args:
        player: Имя атакующего
        name: Цель атаки
        damage: Наносимый урон
        
    Returns:
        tuple: (локальный результат, глобальное уведомление)
    """
    monster = monsters[players[player].coords]
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
            del monsters[players[player].coords]
        else:
            response += f'\n{name} now has {monster.hp}'
            response_all += f'\n{name} now has {monster.hp}'

    return (response, response_all)


async def monster_timer() -> None:
    """Периодическое перемещение монстров (каждые 30 сек)."""
    while True:
        await asyncio.sleep(30)
        if monsters.values():
            while True:
                rnd_monster_coords = random.choice(list(monsters.keys()))
                d = list(directions.keys())[random.randrange(4)]
                new_coords = add_mod_10(rnd_monster_coords, directions[d])
                if new_coords in monsters:
                    continue
                monsters[new_coords] = monsters[rnd_monster_coords]
                del monsters[rnd_monster_coords]

                response_all = monsters[new_coords].name
                response_all += ' moved one cell '
                response_all += d
                for p in players:
                    await players[p].queue.put(response_all)
                    if players[p].coords == new_coords:
                        await players[p].queue.put(encounter(
                            monsters[new_coords].name,
                            monsters[new_coords].msg))
                break


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    """Обработчик TCP-подключений клиентов.
    
    Args:
        reader: Входной поток данных
        writer: Выходной поток данных
    """
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
                            point(int(x), int(y)),
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
    except Exception as e:
        print(e.args)
    finally:
        for p in players:
            if p != me:
                await players[p].queue.put(f'{me} disconnected.')
        writer.write(('closed\n').encode())
        await writer.drain()
        writer.close()
        del players[me]


async def main() -> None:
    """Точка входа для запуска сервера."""
    server = await asyncio.start_server(handle_client, 'localhost', 1337)
    asyncio.create_task(monster_timer())
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
