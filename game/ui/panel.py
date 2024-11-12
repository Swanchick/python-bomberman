from pygame import Surface
from pygame.sprite import Sprite
from uuid import uuid4

from utils import Vector


from ..base_game_object import BaseGameObject


class Panel(Sprite, BaseGameObject):
    def __init__(self, id=None):
        self.image = Surface((32, 32))
        self.rect = self.image.get_rect()

        if id is None:
            self.id = str(uuid4())
        else:
            self.id = id
            
        super().__init__()
    
    def spawn(self):
        ...
    
    def update(self):
        ...
    
    def mouse_button_down(self, pos: Vector):
        ...
    
    def mouse_button_up(self, pos: Vector):
        ...
