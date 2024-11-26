import struct
import random

with open("bytes.bin", 'wb') as f:
    for _ in range(10):
        random_float = random.uniform(-1000, 1000)
        random_bytes = random.randbytes(3)
        random_int = random.randint(-2**31, 2**31 - 1)
        f.write(struct.pack('f3si', random_float, random_bytes, random_int))

with open("bytes.bin", 'rb') as infile, open("netbytes.bin", 'wb') as outfile:
        while chunk := infile.read(11):
            unpacked = struct.unpack('f3si', chunk)
            float_val, bytes_val, int_val = unpacked
            network_data = struct.pack('>f3sI', float_val, bytes_val, int_val)
            outfile.write(network_data)