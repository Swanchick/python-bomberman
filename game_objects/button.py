from pygame import Surface
from pygame.font import get_default_font

from game.ui.panel import Panel
from game.ui.text import Text
from game import LevelBuilder
from utils import Vector


class Button(Panel):
    __text: Text
    __click_function: callable
    
    def __init__(self, text: Text = None, width=200, height=100, id=None):
        super().__init__(id)
        
        self.__click_function = None
        self.__text = text
        if self.__text is None:
            self.__text = Text(32, "Button", (0, 0, 0), get_default_font())
            
        
        self.image = Surface((width, height))
        self.rect = self.image.get_rect()
        self.position = Vector(100, 100)
    
    def register_click(self, function: callable):
        self.__click_function = function

    def update(self):
        self.image.fill((255, 0, 0))
        
        self.__text.draw(self.image, Vector(self.image.get_width() / 2 - self.__text.width / 2, self.image.get_height() / 2 - self.__text.height / 2))
    
    def mouse_button_down(self):
        super().mouse_button_down()
        
        if self.is_hovered():
            self.__current_color = (255, 255, 255)

    def mouse_button_up(self):
        if not self._clicked:
            return
        
        self._clicked = False
        
        if self.is_hovered():
            self.on_click()
        
    def on_click(self):
        if self.__click_function is None:
            return
        
        self.__click_function()
    
    @property
    def width(self) -> int:
        return self.image.get_width()
    
    @property
    def height(self) -> int:
        return self.image.get_height()
    