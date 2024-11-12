from pygame.sprite import Group
from abc import ABC

from utils import Vector
from networking import BaseNetwork
from networking.client import Client

from .base_game import BaseGame

class BaseGameObject(ABC):
    position: Vector
    game: BaseGame
    id: str
    layer: int
    name: str
    
    def __init__(self):
        self.position = Vector.zero()
        self.layer = 1

    def start(self):
        ...
    
    def update(self):
        ...

    def draw(self):
        ...
    
    def stop(self):
        ...
        
    def spawn(self, game_object):
        ...
    
    def setup_properties(self, **kwargs):
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
    def layer(self) -> int:
        return
    
    @property
    def id(self) -> str:
        return
