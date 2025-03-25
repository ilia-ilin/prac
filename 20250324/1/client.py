#MUD-client
import asyncio
import sys
import cmd
import cowsay
import readline
import threading
from io import StringIO

weaponsDmg = { 'sword': 10, 'spear': 15, 'axe': 20 }
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

class MUD(cmd.Cmd):
    intro = '<<< Welcome to Python-MUD 0.1 >>>'
    prompt = 'MUD>> '

    def __init__(self):
        super().__init__()
        self.playerName = sys.argv[1]
        self.chat_loop = None
        self.chat_queue = None
    
    def preloop(self):
        pass
        # self.loop.run_until_complete(self._preloop())

    # async def _preloop(self):
    #     pass
    
    def send(self, msg: str):
        if self.chat_loop and self.chat_queue:
            self.chat_loop.call_soon_threadsafe(
                self.chat_queue.put_nowait, 
                msg
            ) 

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
        except Exception as e:
            print("Invalid arguments")

    def complete_addmon(self, text, line, begidx, endidx):
        all_monsters = cowsay.list_cows() + list(customMonsters.keys())
        if len(line.split(' ')) < 3:
            return [name for name in all_monsters if name.startswith(text)]
        else:
            return [name for name in ['coords', 'hello', 'hp'] if name.startswith(text)]
    
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
        except Exception as e:
            print("Invalid arguments")

    def complete_attack(self, text, line, begidx, endidx):
        all_monsters = cowsay.list_cows() + list(customMonsters.keys())
        if len(line.split(' ')) == 2:
            return [name for name in all_monsters if name.startswith(text)]
        elif len(line.split(' ')) == 3:
            return ['with']
        else:
            return [name for name in list(weaponsDmg.keys()) if name.startswith(text)]

async def local_srv(cmdline: MUD):
    reader, writer = await asyncio.open_connection('localhost', 1337)

    writer.write((f'{sys.argv[1]}\n').encode())
    resp = await reader.readline()
    resp = resp.decode().strip()
    if resp == 'error':
        print('Player already exist!')
        writer.close()
        await writer.wait_closed()
        exit(0)
    send_task = asyncio.create_task(cmdline.chat_queue.get())
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
                    send_task = asyncio.create_task(cmdline.chat_queue.get())
                    
                elif task is receive_task:
                    response = task.result().decode().strip()
                    print(f'{response}\n{cmdline.prompt}{readline.get_line_buffer()}', end='', flush=True)
                    receive_task = asyncio.create_task(reader.readline())
                    
    finally:
        send_task.cancel()
        receive_task.cancel()
        writer.close()
        await writer.wait_closed()

def run_local_srv_in_thread(mud: MUD):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mud.chat_queue = asyncio.Queue()
    mud.chat_loop = loop
    loop.run_until_complete(local_srv(mud))

def main():
    if len(sys.argv) < 2:
        print("Get name!")
        return

    cmdline = MUD()
    thread = threading.Thread(target=run_local_srv_in_thread, args=(cmdline,))
    thread.start()
    cmdline.cmdloop()

if __name__ == '__main__':
    main()