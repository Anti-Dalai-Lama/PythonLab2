"""Во входной строке изменить все десятичные записи чисел на шестнадцатиричные и наоборот"""

import re

def hextodec_and_reverse(string):

    def transform(numb):
        hex_lit = ['a','b','c','d','e','f','A','B','C','D','E','F']
        flag = False
        for el in hex_lit:
            if(el in numb.group()):
                flag = True
        if(flag):
            print(numb.group())
            return str(int(numb.group(), 16))
        else:
            return hex(int(numb.group()))[2:]

    res = re.sub(r'[\da-fA-F]+', transform, string)
    return res

res = hextodec_and_reverse("ab123xasfast15ttf")
print(res)