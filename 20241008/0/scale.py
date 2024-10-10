def scale(x, startIn, endIn, startOut, endOut):
    return (x - startIn) * (startOut - endOut) / (startIn - endIn) + startOut
