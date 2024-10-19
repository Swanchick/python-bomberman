from pygame.sprite import Group

from abc import ABC
from utils import Vector
from networking import BaseNetwork


class GameObjectAbstract(ABC):
    network: BaseNetwork
    current_game: Group

    @property
    def position(self) -> Vector:
        return

    @property
    def layer(self) -> int:
        return
