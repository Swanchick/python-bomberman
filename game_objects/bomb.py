from pygame import Surface

from game.collider_type import ColliderType
from utils import Vector

from .network.network_object import NetworkObject, register_network_class


@register_network_class
class Bomb(NetworkObject):
    def start(self):
        self._layer = -1
        self.size = 64
        
        self.surface = Surface((self.size, self.size))
        self.set_collider(ColliderType.BLANK)
    
    def setup_properties(self, **properties):
        position = properties.get("position", (0, 0))
        
        self.position = (Vector(position[0], position[1]) / 64).round() * 64
    
    def get_data_to_sync(self):
        return {
            "position": [int(self.position.x), int(self.position.y)]
        }
    
    def sync_data(self, data):
        position = data.get("position")
        
        if position is None:
            return
        
        self.position = Vector(position[0], position[1])
    
    def update(self):
        ...



