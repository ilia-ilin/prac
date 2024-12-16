from itertools import count
from asyncio import sleep, Future, gather, run
from collections import deque

stopEvent = Future()

async def writer(que: deque, dl):
    for i in count(0, 1):
        if stopEvent.done():
            break
        await sleep(dl)
        que.append(f"{i}_{dl}")

async def stacker(que: deque, stk: deque):
    while True:
        if stopEvent.done():
            break
        if len(que) > 0:
            stk.append(que.popleft())
        else:
            await sleep(0)

async def reader(stk: deque, n, dl):
    while n > 0:
        await sleep(dl)
        if len(stk) > 0:
            print(stk.pop())
            n -= 1
    stopEvent.set_result(None)

stk, que = deque(), deque()

async def main():
    dl1, dl2, dl3, n = eval(input())
    await gather(
        writer(que, dl1),
        writer(que, dl2),
        stacker(que, stk),
        reader(stk, n, dl3)
    )

run(main())