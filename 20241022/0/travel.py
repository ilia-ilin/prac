def travel(n):
    for _ in range(n):
        yield "по кочкам"
    return "и в яму"
def travelwrap(n):
    rtrn = yield from travel(n)
    yield rtrn
