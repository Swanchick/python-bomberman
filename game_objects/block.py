from pygame import Surface
from pygame.image import load as image_load

from game.game_object import GameObject
from game.level_builder import LevelBuilder


@LevelBuilder.register_object
class Block(GameObject):    
    def setup_properties(self, **properties):
        super().setup_properties(**properties)
        
        texture = properties.get("texture")
        if texture is None:
            return
        
        self.image = image_load(texture)
        self.rect = self.image.get_rect()
