from typing import Self


class Vector:
    __x: int
    __y: int

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def lerp(self, to, t) -> Self:
        new_x = self.__x + (to.x - self.__x) * t
        new_y = self.__y + (to.y - self.__y) * t
        return Vector(new_x, new_y)

    @staticmethod
    def zero():
        return Vector(0, 0)
    
    @staticmethod
    def one():
        return Vector(1, 1)

    @property
    def x(self) -> int:
        return self.__x
    
    @property
    def y(self) -> int:
        return self.__y
    

    