from pygame.sprite import Group
from abc import ABC
from typing import Self

from utils import Vector
from networking import BaseNetwork
from networking.client import Client

from .base_game import BaseGame

class BaseGameObject(ABC):
    position: Vector
    game: BaseGame
    
    def start(self):
        ...
    
    def update(self):
        ...

    def draw(self):
        ...
    
    def stop(self):
        ...
        
    def spawn(self, game_object: Self):
        ...
    
    def setup_properties(self, **kwargs):
        ...
    
    @property
    def layer(self) -> int:
        return
