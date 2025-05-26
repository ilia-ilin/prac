# MUD-client
import sys
import threading
from mood.client import MUD, run_local_srv_in_thread


def find(lst: list, sub: str) -> int:
    try:
        return lst.index(sub)
    except ValueError:
        return -1


def main():
    if len(sys.argv) < 2:
        print("Get name!")
        return

    fileIdx, ipIdx = find(sys.argv, '--file'), find(sys.argv, '--ip')
    if ipIdx >= 0:
        ip = sys.argv[ipIdx + 1]
    else:
        ip = None
    if fileIdx >= 0:
        with open(sys.argv[fileIdx + 1], 'r') as file:
            cmdline = MUD(sys.argv[1], file, 1.0)
            thread = threading.Thread(target=run_local_srv_in_thread, args=(cmdline, sys.argv[1], ip))
            thread.start()
            cmdline.cmdloop()
    else:
        cmdline = MUD(sys.argv[1])
        thread = threading.Thread(target=run_local_srv_in_thread, args=(cmdline, sys.argv[1], ip))
        thread.start()
        cmdline.cmdloop()


if __name__ == '__main__':
    main()
