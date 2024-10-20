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

        self.__network.register_on_connect(self.on_player_connected)
        self.__network.register_on_receive(self.on_player_data_receive)


        player = Player()

        self.add(player)

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
    
    def on_player_connected(self, client):
        print(client.name)

        self.__network.broadcast("create-player", {}, client)

    def on_player_data_receive(self, action, client, data):
        if self.__network.is_server():
            if action == "position-sync":
                self.__network.broadcast("position-sync", data, client)

        if self.__network.is_client():
            if action == "create-player":
                if client is None:
                    return

                print(f"{client.name} {client.id}")

                new_player = Player()
                new_player.network = ProxyNetwork(client)
                print(new_player.network.is_proxy())
                new_player.current_game = self
                self.add(new_player)

    def stop(self):
        self.__network.stop()

    @property
    def network(self) -> BaseNetwork:
        return self.__network 
