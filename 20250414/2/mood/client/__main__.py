# MUD-client
import asyncio
import sys
import cmd
import cowsay
import readline
import threading

weaponsDmg = {'sword': 10, 'spear': 15, 'axe': 20}
customMonsters = ["jgsbat"]


class MUD(cmd.Cmd):
    intro = '<<< Welcome to Python-MUD 0.1 >>>'
    prompt = 'MUD>> '

    def __init__(self, name, stdin=None, delay=None):

        self.use_rawinput = stdin is None

        self.playerName = name
        self.delay = delay

        super().__init__(stdin=stdin)

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.local_srv_loop = None
        self.local_srv_queue = None
        self.close_event = None

    def postcmd(self, stop, line):
        if self.close_event.is_set():
            return True
        return super().postcmd(stop, line)

    def send(self, msg: str):
        if self.local_srv_loop and self.local_srv_queue:
            self.local_srv_loop.call_soon_threadsafe(
                self.local_srv_queue.put_nowait,
                msg
            )
            if self.delay:
                self.loop.run_until_complete(asyncio.sleep(self.delay))
        else:
            exit(0)

    def do_up(self, arg):
        "Move up"
        self.move_player(0, -1)

    def do_down(self, arg):
        "Move down"
        self.move_player(0, 1)

    def do_left(self, arg):
        "Move left"
        self.move_player(-1, 0)

    def do_right(self, arg):
        "Move right"
        self.move_player(1, 0)

    def move_player(self, dx, dy):
        self.send(f"move {dx} {dy}")

    def do_addmon(self, arg):
        """
        Add a monster
        Syntax: addmon name hp <number> coords <x> <y> hello "Message"
        """
        try:
            tokens = arg.split(' ')
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

            if name not in cowsay.list_cows() and name not in customMonsters:
                print('Cannot add unknown monster')
                return

            self.send(f"addmon {name} {x} {y} {hp} {msg}")
        except Exception:
            print("Invalid arguments")

    def complete_addmon(self, text, line, begidx, endidx):
        all_monsters = cowsay.list_cows() + customMonsters
        if len(line.split(' ')) < 3:
            return [name for name in all_monsters if name.startswith(text)]
        else:
            return [name for name in ['coords', 'hello', 'hp']
                    if name.startswith(text)]

    def do_attack(self, arg):
        "Attack a monster"
        try:
            tokens = arg.split(' ')
            name = tokens[0]
            if not name:
                print("Invalid arguments")
                return

            if len(tokens) == 1:
                damage = weaponsDmg['sword']
            elif tokens[1] == 'with':
                if tokens[2] not in weaponsDmg:
                    print('Unknown weapon')
                    return
                damage = weaponsDmg[tokens[2]]

            self.send(f"attack {name} {damage}")
        except Exception:
            print("Invalid arguments")

    def complete_attack(self, text, line, begidx, endidx):
        all_monsters = cowsay.list_cows() + customMonsters
        if len(line.split(' ')) == 2:
            return [name for name in all_monsters if name.startswith(text)]
        elif len(line.split(' ')) == 3:
            return ['with']
        else:
            return [name for name in list(weaponsDmg.keys())
                    if name.startswith(text)]

    def do_sayall(self, arg):
        "Say all"
        try:
            if ' ' in arg:
                if '"' == arg[0] and '"' == arg[-1]:
                    self.send(f"sayall {arg[1:-1]}")
                else:
                    print("Invalid arguments")
            else:
                self.send(f"sayall {arg}")
        except Exception as e:
            print(e.args)

    def do_EOF(self, arg):
        return True

    def do_movemonsters(self, arg):
        if arg in ['on', 'off']:
            self.send(f"movemonsters {arg}")
        else:
            print("Invalid arguments")

    def complete_movemonsters(self, text, line, begidx, endidx):
        return [name for name in ['on', 'off'] if name.startswith(text)]

    def do_locale(self, arg):
        if not arg or ' ' in arg:
            print("Invalid arguments")
        else:
            self.send(f"locale {arg}")


async def local_srv(cmdline: MUD):
    try:
        reader, writer = await asyncio.open_connection('localhost', 1337)
    except Exception:
        cmdline.close_event.set()
        print('server is closed!')
        exit(0)

    writer.write((f'{sys.argv[1]}\n').encode())
    resp = await reader.readline()
    resp = resp.decode().strip()

    if resp == 'error':
        cmdline.close_event.set()
        print('Player already exist!')
        writer.close()
        await writer.wait_closed()
        exit(0)

    send_task = asyncio.create_task(cmdline.local_srv_queue.get())
    receive_task = asyncio.create_task(reader.readline())

    try:
        while True:
            done, pending = await asyncio.wait(
                [send_task, receive_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                if task is send_task:
                    data = task.result()
                    writer.write(f"{data}\n".encode())
                    await writer.drain()
                    send_task = asyncio.create_task(
                        cmdline.local_srv_queue.get()
                        )

                elif task is receive_task:
                    response = task.result().decode().strip()
                    if response == 'closed':
                        cmdline.close_event.set()
                        print('Server closed!')
                        raise Exception('close')

                    toPrint = f'\n{response.replace('\\n', '\n')}\n'
                    toPrint += cmdline.prompt
                    toPrint += readline.get_line_buffer()
                    print(toPrint, end='', flush=True)
                    receive_task = asyncio.create_task(reader.readline())

    except Exception as e:
        if e.args[0] != 'close':
            print(e)
    finally:
        send_task.cancel()
        receive_task.cancel()
        writer.close()
        await writer.wait_closed()


def run_local_srv_in_thread(cmdline: MUD):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    cmdline.local_srv_queue = asyncio.Queue()
    cmdline.local_srv_loop = loop
    cmdline.close_event = threading.Event()
    loop.run_until_complete(local_srv(cmdline))


def main():
    if len(sys.argv) < 2:
        print("Get name!")
        return

    if len(sys.argv) >= 4:
        if sys.argv[2] == '--file':
            with open(sys.argv[3], 'r') as file:
                cmdline = MUD(sys.argv[1], file, 1.0)
                thread = threading.Thread(target=run_local_srv_in_thread, args=(cmdline,))
                thread.start()
                cmdline.cmdloop()
        else:
            print('Invalid arguments!')
    else:
        cmdline = MUD(sys.argv[1])
        thread = threading.Thread(target=run_local_srv_in_thread, args=(cmdline,))
        thread.start()
        cmdline.cmdloop()


if __name__ == '__main__':
    main()
