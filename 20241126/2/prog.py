from sys import stdin, stdout


s = b''.join(stdin.buffer.readlines())
stdout.reconfigure(encoding='utf-8')
stdout.write(s.decode("utf-8", errors="replace").encode("latin1", errors="replace").decode("CP1251", errors="replace"))