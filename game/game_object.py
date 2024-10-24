from pygame.sprite import Sprite, Group
from uuid import uuid4

from networking import BaseNetwork, Network, ProxyNetwork
from networking.client import Client
from utils import Vector
from .game_object_abstract import GameObjectAbstract


class GameObject(Sprite, GameObjectAbstract):
    _id: str
    _layer: int

    _position: Vector
    game: Group
    network: BaseNetwork
    
    owner: Client

    def __init__(self, id: str = None, is_proxy: bool = False):
        self._layer = 1
        self.position = Vector.zero()
        if id is None:
            self._id = str(uuid4())
        else:
            self._id = id

        if is_proxy:
            self.network = ProxyNetwork()
        else:
            self.network = Network.get()

        super().__init__()
    
    def start(self):
        ...

    def update(self):
        ...

    def is_server(self) -> bool:
        return self.network.is_server()

    def is_client(self) -> bool:
        return self.network.is_client()

    def is_proxy(self) -> bool:
        return self.network.is_proxy()

    def network_spawn(self, game_object):
        ...

    @property
    def layer(self) -> int:
        return self._layer

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def position(self) -> Vector:
        return self._position

    @position.setter
    def position(self, value: Vector):
        self._position = value
