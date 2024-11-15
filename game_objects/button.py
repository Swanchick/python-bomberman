from pygame import Surface
from pygame.font import get_default_font

from game.ui.panel import Panel
from game.ui.text import Text
from game import LevelBuilder
from utils import Vector

@LevelBuilder.register_object
class Button(Panel):
    __text: Text
    
    def __init__(self, text="Hello World", id=None):
        super().__init__(id)
        
        self.__text = Text(get_default_font(), 16, text, (0, 0, 0))
    
    def start(self):
        self.image = Surface((200, 32))
        self.rect = self.image.get_rect()
        
        self.position = Vector(100, 100)
        
        self.__colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        self.__current_color = self.__colors[0]
        self.__index = 0

    def update(self):
        self.image.fill(self.__current_color)
        
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
            self.__index += 1
            self.__current_color = self.__colors[(self.__index) % len(self.__colors)]
            self.on_click()
        else:
            self.__current_color = self.__colors[0]
            self.__index = 0
        
    def on_click(self):
        print("clicked")
        
        