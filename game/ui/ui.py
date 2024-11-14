from pygame.sprite import AbstractGroup

from ..base_game import BaseGame
from ..base_game_object import BaseGameObject
from .panel import Panel

class UI(AbstractGroup, BaseGame):
    def __init__(self):
        super().__init__()
        self._sprites = []

    def spawn(self, game_object):
        self._sprites.append(game_object)
    
    def start(self):
        panels: list[Panel] = self.sprites()
        
        for panel in panels:
            panel.start()

    def update(self):
        panels: list[Panel] = self.sprites()
        
        for panel in panels:
            panel.rect.x = panel.position.x
            panel.rect.y = panel.position.y
            
            panel.update()
    
    def draw(self, surface, special_flags=1):
        sprites = self.sprites()
        for spr in sprites:
            surface.blit(spr.image, spr.rect)
    
    def mouse_button_down(self):
        panels: list[Panel] = self.sprites()
        
        for panel in panels:
            panel.mouse_button_down()
    
    def mouse_button_up(self):
        panels: list[Panel] = self.sprites()
        
        for panel in panels:
            panel.mouse_button_up()
    
    def remove(self, game_object):
        self._sprites.remove(game_object)

    def sprites(self):
        return self._sprites