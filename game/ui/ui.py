from pygame.sprite import AbstractGroup

from ..base_game import BaseGame
from ..base_game_object import BaseGameObject


class UI(AbstractGroup, BaseGame):
    def __init__(self):
        super().__init__()
        self._sprites = []

    def spawn(self, game_object):
        self._sprites.append(game_object)
    
    def start(self):
        ...

    def update(self):
        for sprite in self._sprites:
            sprite.update()
    
    def draw(self, surface, special_flags):
        game_objects: list[BaseGameObject] = self.sprites()

        game_objects.sort(key=lambda x: x.layer)

        for obj in game_objects:
            self.spritedict[obj] = surface.blit(obj.image, obj.rect, None, special_flags)

        self.lostsprites = []
        dirty = self.lostsprites

        return dirty
    
    def remove(self, game_object):
        self._sprites.remove(game_object)

    def sprites(self):
        return self._sprites