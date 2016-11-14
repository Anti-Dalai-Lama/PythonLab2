"""Реализовать функцию, которая является аналогом reduce для списка, но за один проход может просматривать несколько
 атрибутов класса и применять в каждому свою функцию. К примеру, за один проход можно получить сразу двух студентов:
 у которого возраст максимальный и у которого оценка минимальная"""
import operator

class Student (object):
    def __init__(self, name, age, avg_mark):
        self.name = name
        self.age = age
        self.avg_mark = avg_mark

def finderN(list, attrs, funcs, compared_element = None):
    if(compared_element == None):
        compared_element = list[0]
    l = [None] * len(attrs)
    res = [compared_element] * len(attrs)
    for i in range(0,len(attrs)):
        l[i] = getattr(compared_element, attrs[i])
    for el in list:
        for i in range(0,len(attrs)):
            val = getattr(el, attrs[i])
            if(funcs[i](val, l[i])):
                l[i] = val
                res[i] = el
    for r in res:
        print(r.__dict__)
    return res

list = [Student("Art", 20, 4), Student("Den", 19, 2), Student("Vasya", 21, 5), Student("Den", 19, 1)]
finderN(list,["age", "avg_mark"], [operator.gt, operator.lt])