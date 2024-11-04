from pygame.sprite import Sprite, Group
from uuid import uuid4

from utils import Vector
from .base_game_object import BaseGameObject


class GameObject(Sprite, BaseGameObject):
    _id: str
    _layer: int

    def __init__(self, id: str = None):
        self._layer = 1
        self.position = Vector.zero()

        if id is None:
            self._id = str(uuid4())
        else:
            self._id = id

        super().__init__()
    
    def spawn(self, game_object):
        self.game.spawn(game_object)
    
    @property
    def layer(self) -> int:
        return self._layer

    @property
    def id(self) -> str:
        return self._id
