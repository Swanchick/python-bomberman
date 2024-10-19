from pygame.sprite import Sprite, Group
from uuid import uuid4

from networking import BaseNetwork
from utils import Vector
from .abstract_game_object import GameObjectAbstract


class GameObject(Sprite, GameObjectAbstract):
    _id: str
    _layer: int
    _position: Vector

    current_game: Group
    network: BaseNetwork

    def __init__(self):
        self._layer = 1
        self._position = Vector.zero()
        self._id = str(uuid4())

        super().__init__()

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
