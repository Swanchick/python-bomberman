from pygame.key import get_pressed as get_keys
from pygame import (
    Surface,
    K_a, K_LEFT,
    K_d, K_RIGHT,
    K_w, K_UP,
    K_s, K_DOWN,
    K_SPACE
)
from networking import ProxyNetwork

from networking.client import Client
from utils import Time, Vector
from .network_object import NetworkObject, NETWORK_CLASSES


import math

class Player(NetworkObject):
    __velocity: Vector
    __speed: float

    __position_to: Vector
    __bot: bool
    
    def __init__(self, id: str = None, is_proxy: bool = False, client: Client = None):
        super().__init__(id, is_proxy, client)
        
        self.__position_to = Vector(0, 0)
        self.__bot = False
    
    def set_bot(self, bot):
        self.__bot = bot
    
    def setup_properties(self, **kwargs):
        if "position" in kwargs:
            self.position = Vector(kwargs["position"][0], kwargs["position"][1])
        else:
            self.position = Vector.zero()
    
    def get_data_to_sync(self) -> dict:
        data = {
            "position": [int(self.position.x), int(self.position.y)]
        }
        
        return data
    
    def sync_data(self, data: dict):
        position = data.get("position")
        
        if position is None:
            return
        
        if self.is_proxy():
            self.__position_to = Vector(position[0], position[1]) 
        else:
            self.position = Vector(position[0], position[1])
        
    def start(self):
        self._layer = 1

        self.image = Surface((32, 32))
        self.rect = self.image.get_rect()

        self.__velocity = Vector.zero()
        self.__speed = 400
        
    def update(self):
        super().update()
        
        if self.is_server() and self.__bot:
            self.position.set_x(math.sin(Time.cur_time) * 50)
        
        if self.is_proxy():
            self.image.fill((0, 255, 0))
            self.move_smoothly()
        elif self.is_client():
            self.image.fill((255, 0, 0))
        
            self.controls()
    
    def move_smoothly(self):
        self.position = self.position.lerp(self.__position_to, 10 * Time.delta)
    
    def controls(self):
        keys = get_keys()

        horizontal = int(keys[K_d] or keys[K_RIGHT]) - int(keys[K_a] or keys[K_LEFT])
        vertical = int(keys[K_s] or keys[K_DOWN]) - int(keys[K_w] or keys[K_UP])

        dir = Vector(horizontal, vertical)
        dir.normalize()

        velocity = dir * self.__speed * Time.delta

        self.__velocity = self.__velocity.lerp(velocity, 10 * Time.delta)
        self.position += self.__velocity


NETWORK_CLASSES[Player.__name__] = Player