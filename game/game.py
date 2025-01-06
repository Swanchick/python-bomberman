from pygame import Surface

from game_objects import *
from window import BaseWindow
from utils import Vector


from .base_game_object import BaseGameObject
from .base_game import BaseGame


class Game(BaseGame):
    __window: BaseWindow
    
    __game_objects: list[BaseGameObject]

    def __init__(self, window: BaseWindow):
        self.__window = window

        self.__game_objects = []
    
    def start(self):        
        game_objects: list[BaseGameObject] = self.__game_objects

        for game_object in game_objects:
            game_object.start()

    def update(self):
        game_objects: list[BaseGameObject] = self.__game_objects

        for game_object in game_objects:
            game_object.collider.update(game_object.position)

            game_object.update()       

    def draw(self, surface: Surface, bgsurf=None, special_flags=0):
        game_objects: list[BaseGameObject] = self.__game_objects

        game_objects.sort(key=lambda x: x.layer)

        camera_pos = self.__window.get_camera_pos()
        resolution = self.__window.resolution
        offset = 64*2
    
        for game_object in game_objects:
            if game_object.surface is None:
                continue
            
            game_object_position = game_object.position
            
            if game_object_position.x + offset < -camera_pos.x or game_object_position.x - offset > -camera_pos.x + resolution.x:
                continue
            
            if game_object_position.y + offset < -camera_pos.y or game_object_position.y - offset > -camera_pos.y + resolution.y:
                continue
            
            surface.blit(game_object.surface, (game_object.position.x, game_object.position.y))

    def draw_debug(self, surface: Surface):
        game_objects: list[BaseGameObject] = self.__game_objects

        for game_object in game_objects:
            if game_object.surface is None:
                continue
            
            if game_object.collider.collider_type.value == 2:
                continue

            game_object.draw_debug(surface)

    def spawn(self, game_object: BaseGameObject):
        game_object.game = self
        self.__game_objects.append(game_object)
        
        game_object.start()
    
    def stop(self):
        game_objects: list[BaseGameObject] = self.__game_objects

        for game_object in game_objects:
            game_object.stop()
    
    def remove(self, game_object):
        self.__game_objects.remove(game_object)

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
        return self.__game_objects
