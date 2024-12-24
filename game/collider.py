from .collider_type import ColliderType


class Collider:
    __w: int
    __h: int

    __left: int
    __right: int
    __top: int
    __down: int

    __collider_type: ColliderType

    def __init__(self, collider_type: ColliderType, x: int, y: int, w: int, h: int):
        self.__collider_type = collider_type

        self.__w = w
        self.__h = h
        
        self.update(x, y)
    
    def update(self, x: int, y: int):
        self.__left = x
        self.__right = x + self.w

        self.__top = y
        self.__down = y + self.h

    def set_width(self, w: int):
        self.__w = w
    
    def set_height(self, h: int):
        self.__h = h

    def collide(self, collider) -> bool:
        pass

    @property
    def collider_type(self) -> ColliderType:
        return self.__collider_type
    
    @property
    def width(self) -> int:
        return self.__w
    
    @property
    def height(self) -> int:
        return self.__h

    @property
    def left(self) -> int:
        return self.__left
    
    @property
    def right(self) -> int:
        return self.__right
    
    @property
    def top(self) -> int:
        return self.__top
    
    @property
    def down(self) -> int:
        return self.__down
