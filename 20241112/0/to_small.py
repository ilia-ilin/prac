def div(a, b):
    if b < 100500:
        raise ZeroDivisionError(f"{b} to small number! I think, it is zero!")
    else:
        return a / b
