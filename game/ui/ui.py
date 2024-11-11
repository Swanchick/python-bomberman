from pygame.sprite import AbstractGroup

from ..base_game import BaseGame


class UI(AbstractGroup, BaseGame):
    def __init__(self):
        super().__init__()
        self._sprites = []

    def spawn(self, game_object):
        self._sprites.append(game_object)
    
    def update(self):
        for sprite in self._sprites:
            sprite.update()
    
    def draw(self, screen):
        for sprite in self._sprites:
            sprite.draw(screen)
    
    def remove(self, game_object):
        self._sprites.remove(game_object)

    def sprites(self):
        return self._sprites