from sys import stdin, stdout


s = b''.join(stdin.buffer.readlines())
N = s[0]
tail = s[1:]
L = len(tail)
stdout.buffer.write(N.to_bytes(1) + b''.join(sorted([tail[i * L // N : (i + 1) * L // N] for i in range(N)])))