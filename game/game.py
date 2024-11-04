from pygame.sprite import AbstractGroup

from networking import Network
# from networking.network_keys import *
from game_objects import *

from .base_game_object import BaseGameObject
from .base_game import BaseGame

from game_objects.network_manager import NetworkManager
from game_objects.player import Player

class Game(AbstractGroup, BaseGame):
    def __init__(self):
        super().__init__()

        network = NetworkManager()
        self.spawn(network)
    
    def start(self):        
        game_objects: list[BaseGameObject] = self.sprites()

        for game_object in game_objects:
            game_object.start()

    def update(self):
        game_objects: list[BaseGameObject] = self.sprites()

        for game_object in game_objects:
            game_object.rect.x = game_object.position.x
            game_object.rect.y = game_object.position.y


            game_object.update()       

    def draw(self, surface, bgsurf=None, special_flags=0):
        game_objects: list[BaseGameObject] = self.sprites() 

        game_objects.sort(key=lambda x: x.layer)

        for obj in game_objects:
            self.spritedict[obj] = surface.blit(obj.image, obj.rect, None, special_flags)

        self.lostsprites = []
        dirty = self.lostsprites

        return dirty

    def spawn(self, game_object: BaseGameObject):
        game_object.game = self
        
        super().add(game_object)
        
        game_object.start()

    def stop(self):
        game_objects: list[BaseGameObject] = self.sprites()

        for game_object in game_objects:
            game_object.stop()

    @property
    def gameobjects(self) -> list[BaseGameObject]:
        return self.sprites()
