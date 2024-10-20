from pygame.sprite import AbstractGroup

from .abstract_game_object import GameObjectAbstract

from networking import ClientNetwork, ProxyNetwork, BaseNetwork, Network

from game_objects.player import Player

class Game(AbstractGroup):
    __network: BaseNetwork
    
    def __init__(self):
        super().__init__()
        
        self.__network = Network.get()

        if self.__network is None:
            self.__network = ClientNetwork("127.0.0.1", 50000)
            
            self.__network.init_client()
            self.__network.start()

            Network.set(self.__network)

    def add(self, game_object: GameObjectAbstract):
        game_object.network = self.__network
        game_object.current_game = self
        
        super().add(game_object)

    def start(self):
        game_objects: list[AbstractGroup] = self.sprites()

        for game_object in game_objects:
            game_object.start()

    def update(self):
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

    def stop(self):
        self.__network.stop()

    @property
    def network(self) -> BaseNetwork:
        return self.__network 
