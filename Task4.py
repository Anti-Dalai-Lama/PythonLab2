"""Даны два множества точек на плоскости. Выбрать четыре различные точки первого множества так,
чтобы квадрат с вершинами в этих точках накрывал все точки второго множества и имел
минимальную площадь. Использовать ООП"""

#https://habrahabr.ru/post/144571/ - rotate, intersection
#https://habrahabr.ru/post/144921/ - Graham algorithm

import math

class VectorOperations(object):
    @staticmethod
    def rotate(left, mid, right): # если точка r вектора mr лежит левее вектора lm, то res > 0
        return (mid[0]-left[0])*(right[1]-mid[1])-(mid[1]-left[1])*(right[0]-mid[0]) #векторное произведение a × b = {aybz - azby; azbx - axbz; axby - aybx} > 0 если поворот левый! (смотрим только z координату!))

    @staticmethod
    def has_intersection(p1, p2, x1, x2):
        return VectorOperations.rotate(p1, p2, x1)*VectorOperations.rotate(p1, p2, x2) <=0 and \
               VectorOperations.rotate(x1,x2,p1)*VectorOperations.rotate(x1,x2,p2)<=0 #имеют пересечение в крайней точке

    @staticmethod
    def point_inside_angle(point1, point2, point3, checkpoint):  # can be on the line
        if VectorOperations.rotate(point2, point1, checkpoint) >= 0 or VectorOperations.rotate(point2, point3, checkpoint) <= 0:
            return False
        return True

    @staticmethod
    def vector_module(point1, point2, accuracy):
        return int(math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2)) * accuracy)



class Polygon(object):
    def __init__(self,points):  #O(n*log(n))
        minpoint = min(points, key=lambda x: x[1])
        points.remove(minpoint)
        points.sort(  # сортируем по косинусу угла между вектором (-1,0) и вектором от minpoint до рассматриваемой (убывание)
            key=lambda x: ((-1) * (x[0] - minpoint[0]) + (0) * (x[1] - minpoint[1])) / math.sqrt(
                math.pow((x[0] - minpoint[0]), 2) + math.pow((x[1] - minpoint[1]), 2)))
        points.insert(0,minpoint)

        res = [points[0], points[1]]
        for i in range(2,len(points)):
            while VectorOperations.rotate(res[-2], res[-1], points[i]) < 0:
                del res[-1]
            res.append(points[i])
        self.points = res

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value

    def __len__(self):
        return len(self.points)

    def has_point(self, point):
        startpoint = self.points[0]
        if VectorOperations.point_inside_angle(self.points[-1], startpoint, self.points[1], point) and point != startpoint:
            r = 1
            l = len(self.points) - 1
            if len(self.points) > 3:  #проверяем четырехугольники и больше
                while l - r > 1:
                    q = (r + l) // 2
                    if VectorOperations.rotate(startpoint, self.points[q], point) > 0:
                        r = q
                    else:
                        l = q
            return not VectorOperations.has_intersection(startpoint, point, self.points[l], self.points[r])
        else:
            return False

    def get_external_points(self, points):
        return filter(lambda x: not self.has_point(x), points)

    def includes_polygon(self, polygon):
        for i in range(0, len(polygon.points)):
            if (not self.has_point(polygon[i])):
                return False
        return True


class SquareOperations(object):
    accuracy = 1000
    @staticmethod
    def get_dict_lines_by_length(points):  # создаем словарь key = длина между точками, val = пары точек
        dictionary = {}
        for i in range(0, len(points) - 1):
            for j in range(i + 1, len(points)):
                length = VectorOperations.vector_module(points[j], points[i], SquareOperations.accuracy)
                if (length in dictionary):
                    dictionary[length].append((points[j], points[i]))
                else:
                    dictionary[length] = [(points[j], points[i])]

        dictionary.pop(min(dictionary.items(), key=lambda x: x[0])[0])
        return dictionary

    @staticmethod
    def diagonals_create_square(line1, line2):  # сравниваем длины сторон четырехугольника
        return (VectorOperations.vector_module(line1[0], line2[0], SquareOperations.accuracy) == VectorOperations.vector_module(line1[0], line2[1], SquareOperations.accuracy) \
               == VectorOperations.vector_module(line1[1], line2[0], SquareOperations.accuracy) == VectorOperations.vector_module(line1[1],line2[1], SquareOperations.accuracy) \
               and VectorOperations.vector_module(line1[0], line1[1], SquareOperations.accuracy) == VectorOperations.vector_module(line2[0], line2[1], SquareOperations.accuracy))

    @staticmethod
    def find_min_allowed_square(dictionary, polygon):
        while (len(dictionary) != 0):
            current = dictionary.pop(min(dictionary.items(), key=lambda x: x[0])[0])  # min получает целиком весь элемент по key, беру из этого элемента length и по нему pop value
            if(len(current) > 1):
                square = SquareOperations.get_square(current, polygon)
                if (square != False):
                    return square
        return None

    @staticmethod
    def get_square(lines, polygon):
        for i in range(0, len(lines) - 1):
            for j in range(i + 1, len(lines)):
                if (VectorOperations.has_intersection(lines[i][0], lines[i][1], lines[j][0], lines[j][1]) and SquareOperations.diagonals_create_square(lines[i], lines[j])):
                    if (Polygon([lines[i][0], lines[j][1], lines[i][1], lines[j][0]]).includes_polygon(polygon)):
                        return (lines[i][0], lines[j][1], lines[i][1], lines[j][0])
        return False


def solve_task(squarepoints, points):
    polygon = Polygon(points)
    print("Polygon: ", polygon.points)
    sqlen = squarepoints.__len__()
    squarepoints = list(polygon.get_external_points(squarepoints))
    print("External points: ", squarepoints)
    print("Points deleted: ", sqlen - squarepoints.__len__())
    dictionary = SquareOperations.get_dict_lines_by_length(squarepoints)
    print(dictionary)
    square = SquareOperations.find_min_allowed_square(dictionary, polygon)
    if(square == None):
        print("There is no such square!")
    else:
        print("Square: ", square)


points = [(6, 7), (7,4),(8,7),(8, 10), (9,10),(10,9),(10,6),(11, 8),(12,4), (12, 9)] #[(5, 7), (7,4),(8,7),(8, 11), (9,10),(10,9),(10,6),(11, 8),(12,4), (13, 9)]
squarepoints = [(1, 2), (1,5),(1,13),(4, 1), (4,3),(5,3),(5,9),(5, 11),(6,5), (9, 5), (9, 13),(10,1), (10, 9), (13,3),(13,9), (13, 11), (14,5), (14, 7), (17,5), (17,13), (0,0), (0,15), (15,15), (15,0)]

solve_task(squarepoints, points)