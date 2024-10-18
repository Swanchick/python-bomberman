from abc import ABC
from utils import Vector


class GameObjectAbstract(ABC):
    @property
    def position(self) -> Vector:
        return

    @property
    def layer(self) -> int:
        return
