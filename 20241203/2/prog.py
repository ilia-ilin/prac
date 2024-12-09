from collections import defaultdict
from sys import stdin
from math import inf

text = [s.lstrip() for s in (stdin.read().replace(":", ":\n") + "\nstop").split("\n")]

markers = [m[:-1] for m in text if ':' in m]

tokens = []
for elm in text:
    tokens.append([])
    for token in elm.split():
        try:
            tokens[-1].append(float(token))
        except:
            tokens[-1].append(token)

del text
prog = []

for s in tokens:
    match s:
        case ['stop']:
            prog.append(('stop',))
        case ['store', float(num), rcv]:
            prog.append(('store', num, rcv))
        case ['add' | 'sub' | 'mul' | 'div' as op, src, opr, rcv]:
            prog.append((op, src, opr, rcv))
        case ['ifeq' | 'ifne' | 'ifgt' | 'ifge' | 'iflt' | 'ifle' as cmp, src, opr, marker]:
            if marker not in markers: exit(-1)
            prog.append((cmp, src, opr, marker))
        case ['out', src]:
            prog.append(('out', src))
        case [s]:
            if s[-1] == ':':
                prog.append((s,))

del tokens

markers = { e[0][:-1]:i for i, e in enumerate(prog) if ':' in e[0] }
vars = defaultdict(float)

i = 0
while True:
    match prog[i]:
        case ['stop']:
            exit()
        case ['store', float(num), rcv]:
            vars[rcv] = num
        case ['add', src, opr, rcv]:
            vars[rcv] = vars[src] + vars[opr]
        case ['sub', src, opr, rcv]:
            vars[rcv] = vars[src] - vars[opr]
        case ['mul', src, opr, rcv]:
            vars[rcv] = vars[src] * vars[opr]
        case ['div', src, opr, rcv]:
            try:
                vars[rcv] = vars[src] / vars[opr]
            except:
                vars[rcv] = inf
        case ['ifeq', src, opr, marker]:
            if vars[src] == vars[opr]:
                i = markers[marker]
        case ['ifne', src, opr, marker]:
            if vars[src] != vars[opr]:
                i = markers[marker]
        case ['ifgt', src, opr, marker]:
            if vars[src] > vars[opr]:
                i = markers[marker]
        case ['ifge', src, opr, marker]:
            if vars[src] >= vars[opr]:
                i = markers[marker]
        case ['iflt', src, opr, marker]:
            if vars[src] < vars[opr]:
                i = markers[marker]
        case ['ifle', src, opr, marker]:
            if vars[src] <= vars[opr]:
                i = markers[marker]
        case ['out', src]:
            print(vars[src])
    i += 1
