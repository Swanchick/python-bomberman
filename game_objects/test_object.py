from pygame.key import get_pressed as get_keys

from pygame import (
    Surface,
    K_a, K_LEFT,
    K_d, K_RIGHT,
    K_w, K_UP,
    K_s, K_DOWN,
    K_SPACE
)


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

        self.controls()
        
    def controls(self):
        keys = get_keys()

        horizontal = int(keys[K_d] or keys[K_RIGHT]) - int(keys[K_a] or keys[K_LEFT])
        vertical = int(keys[K_s] or keys[K_DOWN]) - int(keys[K_w] or keys[K_UP])

        dir = Vector(horizontal, vertical)
        dir.normalize()

        self._position += dir * 5
            

