import pickle

class SerCls:
    lst = []
    dct = {}
    num = 0
    st = ""

ser = SerCls()
ser.lst.append(1)
ser.dct["2"] = 2
ser.num += 3
ser.st += "4"

s = pickle.dumps(ser)
del ser
ser1 = pickle.loads(s)

print(ser1.lst, ser1.dct, ser1.num, ser1.st)