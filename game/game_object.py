from pygame import Surface
from uuid import uuid4

from utils import Vector

from .collider import Collider
from .collider_type import ColliderType
from .base_game_object import BaseGameObject


class GameObject(BaseGameObject):
    surface: Surface
    collider: Collider

    def __init__(self, id: str = None):
        self.surface = None
        self.collider = Collider(ColliderType.BLANK, Vector.zero(), 32, 32)
        self.position = Vector.zero()

        if id is None:
            self.id = str(uuid4())
        else:
            self.id = id
    
    def set_collider(self, collider_type: ColliderType):
        if self.surface == None:
            return

        self.collider = Collider(collider_type, self.position, self.surface.get_width(), self.surface.get_height())

    def setup_properties(self, **properties):
        position = properties.get("position", [0, 0])
        self.position = Vector(position[0], position[1])
        self._layer = properties.get("layer", -1)
        self.name = properties.get("name", "gameobject")

    def draw_debug(self, surface):
        if self.collider is None:
            return
        
        self.collider.draw(surface)

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
