from pygame.sprite import Sprite, Group
from pygame import Surface
from uuid import uuid4

from utils import Vector
from .base_game_object import BaseGameObject


class GameObject(Sprite, BaseGameObject):
    _id: str
    _layer: int

    def __init__(self, id: str = None):
        self.image = Surface((32, 32))
        self.rect = self.image.get_rect()
        
        self._layer = 1
        self.position = Vector.zero()

        if id is None:
            self._id = str(uuid4())
        else:
            self._id = id

        super().__init__()
    
    def setup_properties(self, **properties):
        position = properties.get("position", [0, 0])
        self.position = Vector(position[0], position[1])
        
        self._layer = properties.get("layer", -1)
    
    def spawn(self, game_object):
        self.game.spawn(game_object)
    
    @property
    def layer(self) -> int:
        return self._layer

    @property
    def id(self) -> str:
        return self._id
