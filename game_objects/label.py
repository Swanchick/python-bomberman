from enum import Enum

from pygame import Surface, SRCALPHA
from pygame.font import get_default_font

from game.ui.panel import Panel
from game.ui.text import Text
from utils import Vector


class LabelAlignment(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class Label(Panel):
    __text: Text
    __label_alignment: LabelAlignment
    
    def __init__(self, text: Text = None, alignment: LabelAlignment = LabelAlignment.LEFT, id=None):
        super().__init__(id)
        
        self.__text = text
        if self.__text is None:
            self.__text = Text(32, "Button", (0, 0, 0), get_default_font())
        
        self.__label_alignment = alignment

    def start(self):
        self.image = Surface((self.__text.width, self.__text.height), SRCALPHA)
        self.rect = self.image.get_rect()

    def update(self):
        self.image.fill((0, 0, 0, 0))
        
        pos_y = self.image.get_height() / 2 - self.__text.height / 2
        
        match self.__label_alignment:
            case LabelAlignment.LEFT:
                self.__text.draw(self.image, Vector(0, pos_y))
            case LabelAlignment.CENTER:
                self.__text.draw(self.image, Vector(self.image.get_width() / 2 - self.__text.width / 2, pos_y))     
            case LabelAlignment.RIGHT:
                self.__text.draw(self.image, Vector(self.image.get_width() - self.__text.width, pos_y))   
        