from pygame import Surface

from game.game_object import GameObject
from utils import Vector
from networking import ServerCommand
from networking.network_keys import *

from .player import Player


class OnClientConnect(ServerCommand):
    def __init__(self, server_network, game):
        super().__init__(server_network)
        self.__game = game
    
    def execute(self, message_protocol, socket):
        client_id = message_protocol.client["id"]
        client = self._server_network.get_client(client_id)
        
        
        player = Player()
        self.__game.spawn(player, client)

        data = {
            "gameobject_name": player.__class__.__name__,
            "gameobject_id": player.id,
        }
        
        print("Hello World")

        self._server_network.broadcast(SPAWN_OBJECT, data, client)


class PlayerSpawn(GameObject):

    def __init__(self, *args):
        super().__init__(*args)

        self._position = Vector(100, 100)
        self._layer = 0

        self.image = Surface((32, 32))
        self.rect = self.image.get_rect()

    def start(self):
        if not self.is_server():
            return
        
        self.game.register(ON_CLINET_INITIALIZE, OnClientConnect(self.network, self.game))
        print("Hello World")

    def update(self):
        self.image.fill((0, 255, 0))