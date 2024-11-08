from abc import ABC
from pygame.sprite import Sprite


class BaseGame(ABC):
    def spawn(self, game_object):        
        ...
    
    def remove(self, game_object):
        ...
    
    def sprites(self) -> list[Sprite]:
        ...