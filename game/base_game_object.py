from pygame import Surface
from abc import ABC

from utils import Vector

from .base_game import BaseGame
from .collider import Collider


class BaseGameObject(ABC):
    _layer: int

    position: Vector
    game: BaseGame
    id: str
    name: str

    surface: Surface

    collider: Collider

    def start(self):
        ...
    
    def update(self):
        ...

    def draw(self):
        ...
    
    def draw_debug(self, surface):
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
    def layer(self):
        return self._layer
    