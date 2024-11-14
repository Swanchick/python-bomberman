from pygame import Surface
from pygame.mouse import get_pos
from pygame.sprite import Sprite
from uuid import uuid4

from utils import Vector


from ..base_game_object import BaseGameObject


class Panel(Sprite, BaseGameObject):
    __clicked: bool
    
    def __init__(self, id=None):
        self.image = Surface((32, 32))
        self.rect = self.image.get_rect()
        
        self.position = Vector.zero()
        
        self.__clicked = False

        if id is None:
            self.id = str(uuid4())
        else:
            self.id = id
            
        super().__init__()
    
    def setup_properties(self, **properties):
        pos = properties.get("position", [0, 0])
        self.position = Vector(pos[0], pos[1])
        
        self._layer = properties.get("layer", -1)
        self.name = properties.get("name", "panel")
    
    def spawn(self):
        ...
    
    def update(self):
        ...
    
    def mouse_button_down(self):
        if self.is_hovered():
            self.__clicked = True
            
    
    def mouse_button_up(self):
        if self.__clicked:
            self.__clicked = False
    
    def is_hovered(self) -> bool:
        pos = get_pos()
        width = self.rect.width
        height = self.rect.height
        
        return (self.position.x < pos[0] < self.position.x + width) and (self.position.y < pos[1] < self.position.y + height)
