from pygame.sprite import AbstractGroup

from .abstract_game_object import GameObjectAbstract

class GameObjectManager(AbstractGroup):
    def __init__(self):
        super().__init__()

    def add(self, game_object: GameObjectAbstract):
        super().add(game_object)

    def start(self):
        game_objects: list[AbstractGroup] = self.sprites()

        for game_object in game_objects:
            game_object.start()

    def update(self,):
        game_objects: list[AbstractGroup] = self.sprites()

        for game_object in game_objects:
            game_object.rect.x = game_object.position.x
            game_object.rect.y = game_object.position.y

            game_object.update()

    def draw(self, surface, bgsurf=None, special_flags=0):
        game_objects: list[AbstractGroup] = self.sprites()

        game_objects.sort(key=lambda x: x.layer)

        for obj in game_objects:
            self.spritedict[obj] = surface.blit(obj.image, obj.rect, None, special_flags)

        self.lostsprites = []
        dirty = self.lostsprites

        return dirty
