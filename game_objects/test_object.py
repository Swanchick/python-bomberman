from pygame import Surface

from game.game_object import GameObject
from utils import Vector


class TestObject(GameObject):
    def __init__(self):
        super().__init__()

        self._position = Vector(100, 100)

        self.image = Surface((100, 100))
        self.rect = self.image.get_rect()

    def update(self):
        self.image.fill((255, 0, 0))
        
        
            

