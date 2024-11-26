txt = "Вопрос"
print(txt.encode('WINDOWS-1251').decode('KOI8-R'))
txt = "бМХЛЮМХЕ"
print(txt.encode("koi8-r").decode("cp1251"))
txt = "ОХРЮМХЕ"
print(txt.encode("koi8-r").decode("cp1251"))