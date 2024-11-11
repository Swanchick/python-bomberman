from pygame.sprite import AbstractGroup

from game_objects import *
from window import BaseWindow

from .base_game_object import BaseGameObject
from .base_game import BaseGame


class Game(AbstractGroup, BaseGame):
    __window: BaseWindow
    
    def __init__(self, window: BaseWindow):
        super().__init__()

        self.__window = window
    
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
    
    def set_camera_pos(self, pos):
        self.__window.set_camera_pos(pos)
    
    def set_camera_scale(self, scale):
        self.__window.set_camera_scale(scale)
    
    def get_camera_pos(self):
        return self.__window.get_camera_pos()

    def get_camera_scale(self):
        return self.__window.get_camera_scale()
    
    @property
    def gameobjects(self) -> list[BaseGameObject]:
        return self.sprites()
