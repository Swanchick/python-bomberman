from pygame import Surface 
from pygame.font import Font

from utils import Vector

class Text:
    __text_surface: Surface
    __font: Font
    __text: str
    __color: tuple[int, int, int]
    
    def __init__(self, font: str, size: int, text: str, color: tuple[int, int, int]):
        self.__font = Font(font, size)
        self.__text = text
        self.__color = color
        
        self.__text_surface = self.__font.render(self.__text, True, color)
    
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
        return self.__text_surface.get_width()
    
    @property
    def height(self) -> int:
        return self.__text_surface.get_height()
    
    @property
    def text(self) -> str:
        return self.__text

    @property
    def color(self) -> tuple[int, int, int]:
        return self.__color
