match int(input()):
    case 1:
        print("one")
    case 2:
        print("two")
    case 3:
        print("three")
    case var if var % 2 == 0:
        print("chet")
    case var:
        print(var, "is to many")
