from pygame import Surface

from game.ui.panel import Panel
from game import LevelBuilder
from utils import Vector

@LevelBuilder.register_object
class TestPanel(Panel):
    def start(self):
        self.image = Surface((100, 32))
        self.rect = self.image.get_rect()
        
        self.position = Vector(100, 100)
        
        self.__colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        self.__current_color = self.__colors[0]
        self.__index = 0
        
        self.__clicked = True
    
    def update(self):
        self.image.fill(self.__current_color)
    
    def mouse_button_down(self):
        if self.is_hovered():
            self.__current_color = (255, 255, 255)
            self.__clicked = True
            
            
    def mouse_button_up(self):
        if not self.__clicked:
            return
        self.__clicked = False
        
        if self.is_hovered():
            self.__index += 1
            self.__current_color = self.__colors[(self.__index) % len(self.__colors)]
        else:
            self.__current_color = self.__colors[0]
            self.__index = 0
        
        