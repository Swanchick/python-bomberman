from pygame.key import get_pressed as get_keys
from pygame.sprite import collide_rect
from pygame.rect import Rect
from pygame import (
    Surface,
    K_a, K_LEFT,
    K_d, K_RIGHT,
    K_w, K_UP,
    K_s, K_DOWN,
    K_SPACE
)

from game.base_game_object import BaseGameObject
from game.level_builder import LevelBuilder


from networking.client import Client
from utils import Time, Vector

from .network_object import NetworkObject, register_network_class
from .block import Block


WIDTH = 800
HEIGHT = 600

@register_network_class
class Player(NetworkObject):
    __velocity: Vector
    __speed: float

    __position_to: Vector
    __camera_pos_to: Vector
    
    def __init__(self, id: str = None, is_proxy: bool = False, client: Client = None):
        super().__init__(id, is_proxy, client)
        self.__camera_pos_to = Vector.zero()
    
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
        self.size = 32

        self.__position_to = self.position
        
        self.image = Surface((self.size, self.size))
        self.rect = self.image.get_rect()

        self.__velocity = Vector.zero()
        self.__speed = 400
        
    def update(self):
        super().update()
        
        if self.is_proxy():
            self.image.fill((0, 255, 0))
            self.move_smoothly()
        elif self.is_client():
            self.image.fill((255, 0, 0))
            self.move_camera()
            self.controls()
    
    def move_smoothly(self):
        self.position = self.position.lerp(self.__position_to, 10 * Time.delta)
    
    def move_camera(self):
        camera_pos = Vector.zero()
        scale = self.get_camera_scale()

        camera_pos.set_x(-self.position.x + (WIDTH // scale.x) // 2 - self.size // 2)
        camera_pos.set_y(-self.position.y + (HEIGHT // scale.y) // 2 - self.size // 2)

        self.__camera_pos_to = self.__camera_pos_to.lerp(camera_pos, Time.delta * 10)

        self.set_camera_pos(self.__camera_pos_to)

    def controls(self):
        keys = get_keys()

        horizontal = int(keys[K_d] or keys[K_RIGHT]) - int(keys[K_a] or keys[K_LEFT])
        vertical = int(keys[K_s] or keys[K_DOWN]) - int(keys[K_w] or keys[K_UP])

        direction = Vector(horizontal, vertical)
        if direction.magnitude != 0:
            direction.normalize()

        velocity = direction * self.__speed * Time.delta

        self.__velocity = self.__velocity.lerp(velocity, Time.delta * 10)
        self.__velocity = self.collide(self.__velocity)

        self.position += self.__velocity

    def collide(self, velocity: Vector) -> Vector:
        adjusted_velocity = Vector(velocity.x, velocity.y) 

        player_left = self.position.x
        player_right = self.position.x + self.size
        player_top = self.position.y
        player_bottom = self.position.y + self.size

        game_objects: list[BaseGameObject] = self.game.sprites()

        for game_object in game_objects:
            if not isinstance(game_object, Block):
                continue

            block_left = game_object.position.x
            block_right = game_object.position.x + 64
            block_top = game_object.position.y
            block_bottom = game_object.position.y + 64

            future_left = player_left + adjusted_velocity.x
            future_right = player_right + adjusted_velocity.x

            if future_right > block_left and future_left < block_right:
                if player_bottom > block_top and player_top < block_bottom:
                    if adjusted_velocity.x > 0:
                        adjusted_velocity.set_x(block_left - player_right)
                    elif adjusted_velocity.x < 0:
                        adjusted_velocity.set_x(block_right - player_left)

            future_top = player_top + adjusted_velocity.y
            future_bottom = player_bottom + adjusted_velocity.y

            if future_bottom > block_top and future_top < block_bottom:
                if player_right > block_left and player_left < block_right:
                    if adjusted_velocity.y > 0:
                        adjusted_velocity.set_y(block_top - player_bottom)
                    elif adjusted_velocity.y < 0:
                        adjusted_velocity.set_y(block_bottom - player_top)

        return adjusted_velocity