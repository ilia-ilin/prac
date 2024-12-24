import os


for path in filter(lambda x: '2024' in x, os.listdir()):
    for ex in filter(lambda x: x != '0', os.listdir(path)):
        file_lines = [b"[remote]"]
        sz = len(list(filter(lambda x: '.in' in x, os.listdir(path + '/' + ex + '/check'))))
        for i in range(1, sz + 1):
            file_lines.append(f'"Утешева Екатерина:{path}/{ex}/{i}" = []'.encode())
        f = open(path + '/' + ex + '/remote', 'wb')
        f.write(b'\n'.join(file_lines))
        f.close()