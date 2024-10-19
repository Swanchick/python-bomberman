from pygame.sprite import Sprite, Group

from networking import BaseNetwork
from utils import Vector
from .abstract_game_object import GameObjectAbstract


class GameObject(Sprite, GameObjectAbstract):
    _current_group: Group
    _layer: int
    _position: Vector
    _network: BaseNetwork

    def __init__(self):
        self._layer = 1
        self._position = Vector.zero()

        super().__init__()
    
    def add_internal(self, group):
        self._current_group = group

        return super().add_internal(group)

    def start(self):
        pass

    def update(self):
        pass

    @property
    def position(self) -> Vector:
        return self._position

    @property
    def layer(self) -> int:
        return self._layer
