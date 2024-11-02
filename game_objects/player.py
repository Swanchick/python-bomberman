from pygame.key import get_pressed as get_keys
from pygame import (
    Surface,
    K_a, K_LEFT,
    K_d, K_RIGHT,
    K_w, K_UP,
    K_s, K_DOWN,
    K_SPACE
)

from utils import Time, Vector
from game.game_object import GameObject


class Player(GameObject):
    __velocity: Vector
    __speed: float

    def start(self):
        self.position = Vector(200, 100)
        self._layer = 1

        self.image = Surface((32, 32))
        self.rect = self.image.get_rect()

        self.__velocity = Vector.zero()
        self.__speed = 400

    def update(self):
        self.image.fill((255, 0, 0))

        self.controls()
        
    def controls(self):
        keys = get_keys()

        horizontal = int(keys[K_d] or keys[K_RIGHT]) - int(keys[K_a] or keys[K_LEFT])
        vertical = int(keys[K_s] or keys[K_DOWN]) - int(keys[K_w] or keys[K_UP])

        dir = Vector(horizontal, vertical)
        dir.normalize()

        velocity = dir * self.__speed * Time.delta

        self.__velocity = self.__velocity.lerp(velocity, 10 * Time.delta)
        self.position += self.__velocity
