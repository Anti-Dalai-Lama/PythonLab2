"""Создать генератор для получения вершин выпуклого многоугольника максимальной площади, \
который построен на заданом множестве точек"""

import sys
import math

class VectorOperations(object):
    @staticmethod
    def rotate(left, mid, right): # если точка r вектора mr лежит левее вектора lm, то res > 0
        # векторное произведение a × b = {aybz - azby; azbx - axbz; axby - aybx} > 0 если поворот левый!
        return (mid[0]-left[0])*(right[1]-mid[1])-(mid[1]-left[1])*(right[0]-mid[0])


def polygon_generator(points):
    min_y = max_y = points[0]
    min_x = max_x = points[0]
    for i in points:
        if(i[0] > max_x[0]):
            max_x = i
        elif(i[0] < min_x[0]):
            min_x = i
        if(i[1] > max_y[1]):
            max_y = i
        elif(i[1] < min_y[1]):
            min_y = i[1]

    border_points = [max_x, max_y, min_x, min_y]
    points.remove((min_y))
    # https://ru.wikipedia.org/wiki/Timsort
    # сложность сортировки O(n*log(n))
    points.sort(
        # сортируем по косинусу угла между вектором (-1,0) и вектором от minpoint до рассматриваемой (убывание)
        key=lambda x: ((-1) * (x[0] - min_y[0]) + (0) * (x[1] - min_y[1])) / math.sqrt(
            math.pow((x[0] - min_y[0]), 2) + math.pow((x[1] - min_y[1]), 2)))
    points.insert(0, min_y)

    res = [points[0], points[1]]

    for i in range(2, len(points)):
        while VectorOperations.rotate(res[-2], res[-1], points[i]) < 0:
            del res[-1]
        if(points[i] == border_points[0]):
            last = [res.pop()]
            for elements in res:
                yield elements
            res = last
            border_points.pop(0)
        res.append(points[i])
    yield res[0]
    yield res[1]


points = [(-2,-4),(3,-4),(-3,-3),(0,-3),(-1,-1),(4,-2),(0,0),(2,1),(5,1),(-4,2),(-1,2),(2,2),(-2,4),(2,5)]
for el in polygon_generator(points):
    print(el)


