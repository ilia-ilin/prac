from asyncio import Event
from math import ceil, log2
import random

async def merge(A1: list, A2: list, start, middle, finish, event_in1: Event, event_in2: Event, event_out: Event):
    if event_in1:
        await event_in1.wait()
    if event_in2:
        await event_in2.wait()
    i1, i2 = start, middle
    for i in range(start, finish):
        if i1 < middle and i2 < finish:
            if A1[i1] < A1[i2]:
                A2[i] = A1[i1]
                i1 += 1
            else:
                A2[i] = A1[i2]
                i2 += 1
        else:
             break
    
    i1 = i1 if i1 < middle else i2
    for i in range(i, finish):
        A2[i] = A1[i1]
        i1 += 1 
    for i in range(start, finish):
        A1[i] = A2[i]
    #print(f"{A1[start : middle]} + {A1[middle : finish]} -> {A2[start : finish]}\n{start, middle, finish}")
    event_out.set()

async def mtasks(Ain: list):
    events = [None] * len(Ain)
    A = Ain.copy()
    B = A.copy()
    l = 1
    tasks = []
    while l < len(A):
        newevents = []
        n = ceil(len(A) / l) // 2
        if len(events) < 2 * n:
            events.append(None)
        for i in range(0, n):
            newevents.append(Event())
            tasks.append(merge(A, B, 2 * i * l, (2 * i + 1) * l, min(2 * (i + 1) * l, len(A)), events[2 * i], events[2 * i + 1], newevents[i]))
        events = newevents
        l *= 2
    return tasks, B

import sys
exec(sys.stdin.read())