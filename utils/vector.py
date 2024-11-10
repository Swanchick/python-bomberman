from math import sqrt


class Vector(object):
    __x: float
    __y: float

    def __init__(self, x: float, y: float):
        self.__x = x
        self.__y = y

    def __repr__(self):
        return f"Vector({self.__x}, {self.__y})"

    def __mul__(self, other):
        if isinstance(other, Vector):
            self.__x *= other.x
            self.__y *= other.y

            return self

        self.__x *= other
        self.__y *= other
        
        return self
    
    def __add__(self, other):
        if isinstance(other, Vector):
            self.__x += other.x
            self.__y += other.y

            return self
        
        self.__x += other
        self.__y += other

        return self

    def __getitem__(self, index):
        pos = (self.__x, self.__y)
        if index > len(pos):
            raise Exception("Out of index!")

        return pos[index]

    def __tuple__(self):
        return (self.__x, self.__y)

    def lerp(self, to, t: float):
        if not isinstance(to, Vector):
            return self
        
        new_x = self.__x + (to.x - self.__x) * t
        new_y = self.__y + (to.y - self.__y) * t

        return Vector(new_x, new_y)
    
    def normalize(self):
        vec = self.normal

        self.__x = vec.x
        self.__y = vec.y

    @staticmethod
    def zero():
        return Vector(0, 0)
    
    @staticmethod
    def one():
        return Vector(1, 1)

    def set_x(self, value: float):
        self.__x = value
    
    def set_y(self, value: float):
        self.__y = value

    @property
    def x(self) -> float:
        return self.__x
    
    @property
    def y(self) -> float:
        return self.__y
    
    @property
    def magnitude(self) -> float:
        return sqrt(self.__x ** 2 + self.__y ** 2)

    @property
    def normal(self):
        length = self.magnitude
        if length == 0:
            return Vector.zero()

        return Vector(self.__x / length, self.__y / length)
    

    