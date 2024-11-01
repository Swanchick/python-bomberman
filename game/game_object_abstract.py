from pygame.sprite import Group

from abc import ABC
from utils import Vector
from networking import BaseNetwork
from networking.client import Client


class GameObjectAbstract(ABC):
    position: Vector
    network: BaseNetwork
    game: Group
    owner: Client

    def start(self):
        ...
    
    def update(self):
        ...

    def draw(self):
        ...
    
    def stop(self):
        ...

    @property
    def layer(self) -> int:
        return
