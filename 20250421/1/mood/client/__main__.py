# MUD-client
import sys
import threading
from mood.client import MUD, run_local_srv_in_thread


def main():
    if len(sys.argv) < 2:
        print("Get name!")
        return

    if len(sys.argv) >= 4:
        if sys.argv[2] == '--file':
            with open(sys.argv[3], 'r') as file:
                cmdline = MUD(sys.argv[1], file, 1.0)
                thread = threading.Thread(target=run_local_srv_in_thread, args=(cmdline, sys.argv[1]))
                thread.start()
                cmdline.cmdloop()
        else:
            print('Invalid arguments!')
    else:
        cmdline = MUD(sys.argv[1])
        thread = threading.Thread(target=run_local_srv_in_thread, args=(cmdline, sys.argv[1]))
        thread.start()
        cmdline.cmdloop()


if __name__ == '__main__':
    main()
