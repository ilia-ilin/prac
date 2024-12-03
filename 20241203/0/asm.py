while True:
    match input().split():
        case ["mov", a, b]:
            print(f"moving {b} to {a}")
        case ["push" | "pop" as cmd, *reglist]:
            print(f"{cmd}ing {reglist}")
        case [cmd, r1]:
            print(f"making {cmd} with {r1}")
        case _:
            print("Parse error")
