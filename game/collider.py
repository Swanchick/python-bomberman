from pygame.draw import rect as draw_rect
from pygame import Surface


from utils import Vector

from .collider_type import ColliderType

class Collider:
    position: Vector

    w: int
    h: int
    
    collider_type: ColliderType

    __left: int
    __right: int
    __top: int
    __bottom: int

    colliding: bool


    def __init__(self, collider_type: ColliderType, position: Vector, w: int, h: int):
        self.collider_type = collider_type

        self.w = w
        self.h = h
        
        self.update(position)

        self.colliding = False
    
    def update(self, position: Vector):
        self.position = position

        self.__left = position.x
        self.__right = position.x + self.w

        self.__top = position.y
        self.__bottom = position.y + self.h

    def draw(self, surface: Surface):
        color = (0, 0, 255)

        if self.colliding:
            color = (0, 255, 0)

        draw_rect(surface, color, (self.position.x, self.position.y, self.w, self.h), 2)

    def collide_horizontal(self, collider, horizontal: float) -> bool:
        future_right = self.right + horizontal
        future_left = self.left + horizontal
        
        return ((future_right > collider.left) and (future_left < collider.right)) and ((self.bottom > collider.top) and (self.top < collider.bottom))

    def collide_vertical(self, collider, vertical: float) -> bool:
        future_top = self.top + vertical
        future_bottom = self.bottom + vertical
        
        return ((future_bottom > collider.top) and (future_top < collider.bottom)) and ((self.right > collider.left) and (self.left < collider.right))

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
    def bottom(self) -> int:
        return self.__bottom
