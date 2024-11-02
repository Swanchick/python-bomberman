from pygame.sprite import Sprite, Group
from uuid import uuid4

from networking import BaseNetwork, Network, ProxyNetwork
from networking.client import Client
from utils import Vector
from .game_object_abstract import GameObjectAbstract


class GameObject(Sprite, GameObjectAbstract):
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
    
    def start(self):
        ...

    def update(self):
        ...

    def stop(self):
        ...

    @property
    def layer(self) -> int:
        return self._layer

    @property
    def id(self) -> str:
        return self._id
