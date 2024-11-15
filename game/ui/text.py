import math

from pygame import Surface, SRCALPHA
from pygame.font import Font, get_default_font

from utils import Vector, Time

class Text:
    __text_surface: Surface
    __font: Font
    __text: str
    __color: tuple[int, int, int]
    
    def __init__(self, size: int, text: str, color: tuple[int, int, int], font=None):
        self.__font = font if font is not None else Font(get_default_font(), size)
        self.__text = text
        self.__color = color

        self.apply()
    
    def draw(self, surface: Surface, position: Vector):
        surface.blit(self.__text_surface, (position.x, position.y))
    
    def set_text(self, text: str):
        self.__text = text
    
    def set_color(self, color: tuple[int, int, int]):
        self.__color = color
    
    def apply(self):
        self.__text_surface = self.__font.render(self.__text, True, self.__color)

    @property
    def width(self) -> int:
        return self.__font.size(self.__text)[0]
    
    @property
    def height(self) -> int:
        return self.__font.size(self.__text)[1]
    
    @property
    def text(self) -> str:
        return self.__text

    @property
    def color(self) -> tuple[int, int, int]:
        return self.__color
