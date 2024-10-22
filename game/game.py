from pygame.sprite import AbstractGroup

from networking import ClientNetwork, BaseNetwork, Network
from networking.network_keys import *
from game_objects.player_spawn import PlayerSpawn
from protocol import Command

from .game_object_abstract import GameObjectAbstract


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
        
        if self.__network.is_server():
            player_spawn = PlayerSpawn()
            self.add(player_spawn)
            player_spawn.game = self

    def add(self, game_object: GameObjectAbstract):
        game_object.network = self.__network
        game_object.current_game = self
        
        super().add(game_object)

    def start(self):
        game_objects: list[GameObjectAbstract] = self.sprites()

        for game_object in game_objects:
            game_object.start()
                

    def update(self):
        game_objects: list[GameObjectAbstract] = self.sprites()

        for game_object in game_objects:
            game_object.rect.x = game_object.position.x
            game_object.rect.y = game_object.position.y

            game_object.update()
                

    def draw(self, surface, bgsurf=None, special_flags=0):
        game_objects: list[GameObjectAbstract] = self.sprites()

        game_objects.sort(key=lambda x: x.layer)

        for obj in game_objects:
            self.spritedict[obj] = surface.blit(obj.image, obj.rect, None, special_flags)

        self.lostsprites = []
        dirty = self.lostsprites

        return dirty

    def register(self, action: str, command: Command):
        self.__network.register(action, command)

    def network_spawn(self, game_object):
        if self.__network.is_client():
            self.__network.send(SPAWN_OBJECT, {"gameobject_id": game_object.id})

    def stop(self):
        self.__network.stop()

    @property
    def network(self) -> BaseNetwork:
        return self.__network 
