from pygame.sprite import Sprite, Group
from pygame import Surface
from uuid import uuid4

from utils import Vector
from .base_game_object import BaseGameObject


class GameObject(Sprite, BaseGameObject):
    id: str
    layer: int

    def __init__(self, id: str = None):
        self.image = Surface((32, 32))
        self.rect = self.image.get_rect()
        
        self.layer = 1
        self.position = Vector.zero()

        if id is None:
            self.id = str(uuid4())
        else:
            self.id = id

        super().__init__()
    
    def setup_properties(self, **properties):
        position = properties.get("position", [0, 0])
        self.position = Vector(position[0], position[1])
        self.layer = properties.get("layer", -1)
        self.name = properties.get("name", "gameobject")
    
    def spawn(self, game_object):
        self.game.spawn(game_object)
    
    def set_camera_pos(self, pos):
        self.game.set_camera_pos(pos)
    
    def set_camera_scale(self, scale):
        self.game.set_camera_scale(scale)

    def get_camera_pos(self):
        return self.game.get_camera_pos()

    def get_camera_scale(self):
        return self.game.get_camera_scale()
