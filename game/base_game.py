from abc import ABC
from pygame.sprite import Sprite

from utils import Vector

class BaseGame(ABC):
    def start(self):
        ...

    def update(self):
        ...
    
    def draw(self):
        ...

    def spawn(self, game_object):        
        ...
    
    def remove(self, game_object):
        ...
    
    def sprites(self) -> list[Sprite]:
        ...
    
    def set_camera_pos(self, pos: Vector):
        ...
    
    def set_camera_scale(self, scale: Vector):
        ...
    
    def get_camera_pos(self) -> Vector:
        ...
    
    def get_camera_scale(self) -> Vector:
        ...

    @property
    def gameobjects(self):
        ...
