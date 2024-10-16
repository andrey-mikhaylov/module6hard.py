from math import pi, sqrt

Color = tuple[int, int, int]


class Figure:
    sides_count = 0

    def __init__(self, sides, color: Color, filled: bool = False):
        """
        :param sides: список сторон (целые числа)
        :param color: список цветов в формате RGB
        :param filled: закрашенный, bool
        """
        sides = list(sides)
        if not self.__is_valid_sides(sides):
            sides = [1] * len(sides)
        self.__sides = sides
        self.__color = color
        self.filled = filled

    def get_color(self) -> Color:
        """
        :return: список RGB цветов.
        """
        return self.__color


    def set_color(self, r: int, g: int, b: int):
        """
        изменяет атрибут __color на соответствующие значения
        предварительно проверив их на корректность
        Если введены некорректные данные, то цвет остаётся прежним.
        :param r: 
        :param g: 
        :param b: 
        :return:
        """

        def __is_valid_sub_color(c: int) -> bool:
            return 0 <= c <= 255

        def __is_valid_color(r: int, g: int, b: int) -> bool:
            """
            служебный, принимает параметры r, g, b,
            проверяет корректность переданных значений перед установкой нового цвета
            Корректным цвет: все значения r, g и b - целые числа в диапазоне от 0 до 255 (включительно)
            :param r:
            :param g:
            :param b:
            :return:
            """
            return all(map(__is_valid_sub_color, (r, g, b)))

        if __is_valid_color(r, g, b):
            self.__color = r, g, b

    def __is_valid_sides(self, sides):
        """
        служебный
        :param sides: неограниченное кол-во сторон
        :return: True если все стороны целые положительные числа, и кол-во новых сторон совпадает с текущим
                 False - во всех остальных случаях
        """
        if len(sides) != self.sides_count:
            return False

        return all(map(lambda x: x>0, sides))

    def get_sides(self) -> list:
        """
        :return: значение атрибута __sides.
        """
        return self.__sides

    def __len__(self) -> int:
        """
        :return: периметр фигуры
        """
        return sum(self.__sides)

    def set_sides(self, *new_sides):
        """
        :param new_sides: новые стороны
               если их количество не равно sides_count, то не изменять, в противном случае - менять.
        """
        if len(new_sides) != self.sides_count:
            return

        self.__sides = list(new_sides)


class Circle(Figure):
    sides_count = 1

    def __init__(self, color: Color, *sides):
        if len(sides) != self.sides_count:
            sides = [1] * self.sides_count
        super().__init__(sides, color)
        self.__radius = self.__calc_radius(sides[0])

    def get_square(self) -> float:
        """
        :return: площадь круга
        """
        # (можно рассчитать как через длину, так и через радиус).
        return pi * self.__radius ** 2.0

    def __calc_radius(self, side_len: int) -> float:
        """
        # рассчитать радиус исходя из длины окружности (одной единственной стороны).
        :param side_len: длина стороны
        :return: радиус
        """
        return side_len / 2.0 / pi

    def get_radius(self):
        return self.__radius


class Triangle(Figure):
    sides_count = 3

    def __init__(self, color: Color, *sides):
        if len(sides) != self.sides_count:
            sides = [1] * self.sides_count
        super().__init__(sides, color)

    def get_square(self) -> float:
        """
        :return: площадь треугольника
        """
        # по формуле Герона
        a, b, c = self.get_sides()
        p = (a + b + c) / 2.0
        s = sqrt(p * (p - a) * (p - b) * (p - c))
        return s


class Cube(Figure):
    sides_count = 12

    def __init__(self, color: Color, *sides):
        # Переопределить __sides сделав список из 12 одинаковы сторон (передаётся 1 сторона)
        if len(sides) != 1:
            sides = [1] * self.sides_count
        else:
            sides = [sides[0]] * self.sides_count
        super().__init__(sides, color)

    def  get_volume(self):
        """
        :return: объём куба.
        """
        s = self.get_sides()[0]
        return s ** 3


def test_figure():
    f = Figure([], (0, 0, 0), False)
    f = Figure([], (500, 500, 500), True)
    f = Figure([], (-1, -1, -1), True)
    f = Figure([], (-1, -1, -1), True)
    f = Figure([], (1, 2, 3), True)
    if len(f) != 0: raise
    if f.get_sides() != []: raise
    if f.get_color() != (1, 2, 3): raise
    f.sides_count = 3
    f.set_sides(1, 2, 3)
    if f.get_sides() != [1, 2, 3]: raise
    if not f.filled: raise
    f.set_color(5, 6, 7)
    if f.get_color() != (5, 6, 7): raise
    f.set_color(300, 400, 500)
    if f.get_color() != (5, 6, 7): raise
    if len(f) != 1+2+3: raise
    pass

def test_circle():
    c = Circle((2,3,4), -1)
    if c.get_sides() != [1]: raise
    l = 5
    r = 5 / 2.0 / pi
    c = Circle((1,2,3), l)
    if c.get_sides() != [l]: raise
    if c.get_color() != (1, 2, 3): raise
    c.set_color(5, 6, 7)
    if c.get_color() != (5, 6, 7): raise
    if c.get_radius() != r: raise
    if c.get_square() != pi * r ** 2.0: raise
    if len(c) != l: raise
    c.set_sides(6)
    if len(c) != 6: raise
    pass


def test_triangle():
    t = Triangle((1, 2, 3), -1, -2, -3)
    if t.get_sides() != [1, 1, 1]: raise
    t = Triangle((1, 2, 3), 5)
    if t.get_sides() != [1, 1, 1]: raise
    a,b,c = 2,3,4
    t = Triangle((1, 2, 3), a,b,c)
    if t.get_sides() != [2,3,4]: raise
    if t.get_color() != (1, 2, 3): raise
    t.set_color(5, 6, 7)
    if t.get_color() != (5, 6, 7): raise
    p = (a+b+c)/2.0
    s = sqrt(p*(p-a)*(p-b)*(p-c))
    if s != t.get_square(): raise
    if len(t) != a+b+c: raise
    pass


def test_cube():
    c = Cube((1, 2, 3), 5)
    if c.get_volume() != 5 ** 3: raise
    if len(c.get_sides()) != 12: raise
    if len(c) != 5*12: raise
    pass


def test():
    circle1 = Circle((200, 200, 100), 10)  # (Цвет, стороны)
    cube1 = Cube((222, 35, 130), 6)

    # Проверка на изменение цветов:
    circle1.set_color(55, 66, 77)  # Изменится
    print(circle1.get_color())
    cube1.set_color(300, 70, 15)  # Не изменится
    print(cube1.get_color())

    # Проверка на изменение сторон:
    cube1.set_sides(5, 3, 12, 4, 5)  # Не изменится
    print(cube1.get_sides())
    circle1.set_sides(15)  # Изменится
    print(circle1.get_sides())

    # Проверка периметра (круга), это и есть длина:
    print(len(circle1))

    # Проверка объёма (куба):
    print(cube1.get_volume())
    """
Выходные данные (консоль):
[55, 66, 77]
[222, 35, 130]
[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
[15]
15
216
    """

if __name__ == '__main__':
    test_figure()
    test_circle()
    test_triangle()
    test_cube()
    test()

"""
2023/11/12 00:00|Дополнительное практическое задание по модулю*
Дополнительное практическое задание по модулю: "Наследование классов."

Цель: Применить знания полученные в модуле, решив задачу повышенного уровня сложности

Задание "Они все так похожи":
2D? 3D? Даже 4D?.... Настолько глубоко мы заходить конечно же не будем, 4D подождёт, но вот с двумерными и трёхмерными фигурами можем поэкспериментировать.
Вы когда-нибудь задумывались как устроены графические библиотеки для языков программирования?
Безусловно, там выполняются огромные расчёты при помощи вашей видеокарты, но... Что лежит в основе удобного использования таких объектов?

По названию задачи можно понять, что все геометрические фигуры обладают схожими свойствами, такими как: длины сторон, цвет и др.

Давайте попробуем реализовать простейшие классы для некоторых таких фигур и при этом применить наследование (в будущем, изучая сторонние библиотеки, вы будете замечать схожие классы, уже написанные кем-то ранее):

Общее ТЗ:
Реализовать классы Figure(родительский), Circle, Triangle и Cube, объекты которых будут обладать методами изменения размеров, цвета и т.д.
Многие атрибуты и методы должны быть инкапсулированны и для них должны быть написаны интерфейсы взаимодействия (методы) - геттеры и сеттеры.

Подробное ТЗ:

Атрибуты класса Figure: sides_count = 0
Каждый объект класса Figure должен обладать следующими атрибутами:
Атрибуты(инкапсулированные): __sides(список сторон (целые числа)), __color(список цветов в формате RGB)
Атрибуты(публичные): filled(закрашенный, bool)
И методами:
Метод get_color, возвращает список RGB цветов.
Метод __is_valid_color - служебный, принимает параметры r, g, b, который проверяет корректность переданных значений перед установкой нового цвета. Корректным цвет: все значения r, g и b - целые числа в диапазоне от 0 до 255 (включительно).
Метод set_color принимает параметры r, g, b - числа и изменяет атрибут __color на соответствующие значения, предварительно проверив их на корректность. Если введены некорректные данные, то цвет остаётся прежним.
Метод __is_valid_sides - служебный, принимает неограниченное кол-во сторон, возвращает True если все стороны целые положительные числа и кол-во новых сторон совпадает с текущим, False - во всех остальных случаях.
Метод get_sides должен возвращать значение я атрибута __sides.
Метод __len__ должен возвращать периметр фигуры.
Метод set_sides(self, *new_sides) должен принимать новые стороны, если их количество не равно sides_count, то не изменять, в противном случае - менять.

Атрибуты класса Circle: sides_count = 1
Каждый объект класса Circle должен обладать следующими атрибутами и методами:
Все атрибуты и методы класса Figure
Атрибут __radius, рассчитать исходя из длины окружности (одной единственной стороны).
Метод get_square возвращает площадь круга (можно рассчитать как через длину, так и через радиус).

Атрибуты класса Triangle: sides_count = 3
Каждый объект класса Triangle должен обладать следующими атрибутами и методами:
Все атрибуты и методы класса Figure
Метод get_square возвращает площадь треугольника. (можно рассчитать по формуле Герона)

Атрибуты класса Cube: sides_count = 12
Каждый объект класса Cube должен обладать следующими атрибутами и методами:
Все атрибуты и методы класса Figure.
Переопределить __sides сделав список из 12 одинаковы сторон (передаётся 1 сторона)
Метод get_volume, возвращает объём куба.

ВАЖНО!
При создании объектов делайте проверку на количество переданных сторон, если сторон не ровно sides_count, то создать массив с единичными сторонами и в том кол-ве, которое требует фигура.
Пример 1: Circle((200, 200, 100), 10, 15, 6), т.к. сторона у круга всего 1, то его стороны будут - [1]
Пример 2: Triangle((200, 200, 100), 10, 6), т.к. сторон у треугольника 3, то его стороны будут - [1, 1, 1]
Пример 3: Cube((200, 200, 100), 9), т.к. сторон(рёбер) у куба - 12, то его стороны будут - [9, 9, 9, ....., 9] (12)
Пример 4: Cube((200, 200, 100), 9, 12), т.к. сторон(рёбер) у куба - 12, то его стороны будут - [1, 1, 1, ....., 1]

Код для проверки:
circle1 = Circle((200, 200, 100), 10) # (Цвет, стороны)
cube1 = Cube((222, 35, 130), 6)

# Проверка на изменение цветов:
circle1.set_color(55, 66, 77) # Изменится
print(circle1.get_color())
cube1.set_color(300, 70, 15) # Не изменится
print(cube1.get_color())

# Проверка на изменение сторон:
cube1.set_sides(5, 3, 12, 4, 5) # Не изменится
print(cube1.get_sides())
circle1.set_sides(15) # Изменится
print(circle1.get_sides())

# Проверка периметра (круга), это и есть длина:
print(len(circle1))

# Проверка объёма (куба):
print(cube1.get_volume())


Выходные данные (консоль):
[55, 66, 77]
[222, 35, 130]
[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
[15]
15
216

Примечания (рекомендации):
Рекомендуется сделать дополнительные (свои проверки) работы методов объектов каждого класса.
Делайте каждый класс и метод последовательно и проверяйте работу каждой части отдельно.
Для проверки принадлежности к типу рекомендуется использовать функцию isinstance.
Помните, служебные инкапсулированные методы можно и нужно использовать только внутри текущего класса.
Вам не запрещается вводить дополнительные атрибуты и методы, творите, но не переборщите!

Файл с кодом (module6hard.py) прикрепите к домашнему заданию или пришлите ссылку на ваш GitHub репозиторий с файлом решения.
"""