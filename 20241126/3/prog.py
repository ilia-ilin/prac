from sys import stdin

s = b''.join(stdin.buffer.readlines())

if len(s) >= 44 and s[0:4] == b"RIFF" and s[8:12] == b"WAVE" and s[36:40] == b"data":
    print(f"Size={int.from_bytes(s[7:3:-1])}, Type={int.from_bytes(s[21:19:-1])}, Channels={int.from_bytes(s[23:21:-1])}, Rate={int.from_bytes(s[27:23:-1])}, Bits={int.from_bytes(s[35:33:-1])}, Data size={int.from_bytes(s[43:39:-1])}")
else:
    print("No")