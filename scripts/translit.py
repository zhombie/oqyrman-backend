# -*- coding: utf-8 -*-
dic = {"а" : "a", "ә" : "a'", "б" : "b", "в" : "v", "г" : "g",\
       "ғ" : "g'", "д" : "d", "е" : "e", "ё" : "e", "ж" : "j",\
       "з" : "z", "и" : "i'", "й" : "i'", "к" : "k", "қ" : "q",\
       "л" : "l", "м" : "m", "н" : "n", "ң" : "n'", "о" : "o",\
       "ө" : "o'", "п" : "p", "р" : "r", "с" : "s", "т" : "t",\
       "у" : "y'", "ұ" : "u", "ү" : "u'", "ф" : "f", "х" : "h",\
       "һ" : "h", "ц" : "ts", "ч" : "c'", "ш" : "s'", "щ" : "s'",\
       "ъ" : "", "ы" : "y", "і" : "i", "ь" : "", "э" : "e",\
       "ю" : "i'y'", "я" : "i'a", \
       "А" : "A", "Ә" : "A'", "Б" : "B", "В" : "V", "Г" : "G",\
       "Ғ" : "G'", "Д" : "D", "Е" : "E", "Ё" : "E", "Ж" : "J",\
       "З" : "Z", "И" : "I'", "Й" : "I'", "К" : "K", "Қ" : "Q",\
       "Л" : "L", "М" : "M", "Н" : "N", "О" : "O", "Ө" : "O'",\
       "П" : "P", "Р" : "R", "С" : "S", "Т" : "T", "У" : "Y'",\
       "Ұ" : "U", "Ү" : "U'", "Ф" : "F", "Х" : "H", "Ц" : "Ts",\
       "Ч" : "C'", "Ш" : "S'", "Щ" : "S'", "Ы" : "Y", "І" : "I",\
       "Э" : "E", "Ю" : "I'y'", "Я" : "I'a"}

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i.decode("utf-8"), j)
    return text

for i in range(1, 17):
    res = ""
    file = open("content_" + str(i) + ".xhtml", "r") 
    for line in file: 
        res += replace_all(line.decode("utf-8"), dic)

    with open("content_" + str(i) + ".xhtml", "w") as f:   
        f.write(res.encode("utf-8")) 
