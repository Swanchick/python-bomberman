from pygame.key import get_pressed as get_keys
from pygame.sprite import collide_rect
from pygame.draw import (
    rect as draw_rect,
    line as draw_line
)

from pygame import (
    Surface,
    K_a, K_LEFT,
    K_d, K_RIGHT,
    K_w, K_UP,
    K_s, K_DOWN,
    K_SPACE
)

from pygame.joystick import (
    get_count as joystick_get_count,
    Joystick,
    JoystickType
)

from game.base_game_object import BaseGameObject
from game.level_builder import LevelBuilder
from game.collider_type import ColliderType

from networking.client import Client
from utils import Time, Vector

from .game_object_network.network_object import NetworkObject, register_network_class
from .block import Block


WIDTH = 800
HEIGHT = 600



@register_network_class
class Player(NetworkObject):
    __velocity: Vector
    __speed: float

    __position_to: Vector
    __camera_pos_to: Vector

    __joystick_connected: bool
    __joystick: JoystickType
    
    def __init__(self, id: str = None, is_proxy: bool = False, client: Client = None):
        super().__init__(id, is_proxy, client)
        self.__camera_pos_to = Vector.zero()
        self.position = Vector.zero()
        self.__velocity = Vector.zero()
    
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
        
        self.surface = Surface((self.size, self.size))
        self.set_collider(ColliderType.SOLID)

        self.__velocity = Vector.zero()
        self.__speed = 400

        self.__joystick_connected = joystick_get_count() > 0 

        if self.is_client() and self.__joystick_connected:
            self.__joystick = Joystick(0)
        
    def update(self):
        super().update()
        
        if self.is_proxy():
            self.surface.fill((0, 255, 0))
            self.move_smoothly()
        elif self.is_client():
            self.surface.fill((255, 0, 0))
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

        if self.__joystick_connected:
            horizontal = self.__joystick.get_axis(0)
            vertical = self.__joystick.get_axis(1)

        direction = Vector(horizontal, vertical)


        if direction.magnitude != 0 and not self.__joystick_connected:
            direction.normalize()

        velocity = direction * self.__speed * Time.delta
        if self.__joystick_connected and direction.magnitude < 0.5:
            velocity = Vector.zero()

        self.__velocity = self.__velocity.lerp(velocity, Time.delta * 10)
        self.__velocity = self.collide()
        self.position += self.__velocity

    def draw_debug(self, surface):
        super().draw_debug(surface)

        distance = 5

        start_x = self.position.x + self.collider.w / 2
        start_y = self.position.y + self.collider.h / 2

        end_x = self.position.x + self.__velocity.x * distance + self.collider.w / 2
        end_y = self.position.y + self.__velocity.y * distance + self.collider.h / 2

        draw_line(surface, (0, 255, 0), (start_x, start_y), (end_x, end_y))
        draw_rect(surface, (0, 255, 0), (self.position.x + self.__velocity.x * distance, self.position.y + self.__velocity.y * distance, self.size, self.size), 1)

    def collide(self) -> Vector:
        adjusted_velocity = Vector(self.__velocity.x, self.__velocity.y)
        game_objects: list[BaseGameObject] = self.game.gameobjects

        for game_object in game_objects:
            collider = game_object.collider

            if  isinstance(game_object, Player):
                continue

            if collider.collider_type != ColliderType.SOLID:
                continue
                
            if self.collider.collide_horizontal(collider, adjusted_velocity.x):
                collider.colliding = True
                
                if adjusted_velocity.x > 0:
                    adjusted_velocity.set_x(collider.left - self.collider.right)
                
                if adjusted_velocity.x < 0:
                    adjusted_velocity.set_x(collider.right - self.collider.left)

            elif self.collider.collide_vertical(collider, adjusted_velocity.y):
                collider.colliding = True
                
                if adjusted_velocity.y > 0:
                    adjusted_velocity.set_y(collider.top - self.collider.bottom)
                
                if adjusted_velocity.y < 0:
                    adjusted_velocity.set_y(collider.bottom - self.collider.top)
                    
            else:
                collider.colliding = False
        
        return adjusted_velocity