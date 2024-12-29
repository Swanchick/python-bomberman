from pygame import Surface

from game.collider_type import ColliderType

from .game_object_network.network_object import NetworkObject, register_network_class


@register_network_class
class Bomb(NetworkObject):
    def start(self):
        self._layer = 1
        self.size = 64
        
        self.surface = Surface((self.size, self.size))
        self.set_collider(ColliderType.BLANK)
    
    def update(self):
        ...



