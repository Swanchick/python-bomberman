from socket import socket as Socket
from sys import argv
from pygame import Surface

from game.game_object import GameObject
from game.base_game import BaseGame

from networking import BaseNetwork, ServerNetwork, ClientNetwork, Network, ProxyNetwork
from networking.network_commands import ClientCommand, ServerCommand
from networking.network_keys import *

from protocol import MessageHandler, MessageProtocol

from .player import Player
from .network_object import NetworkObject, NETWORK_CLASSES

# Server
class OnClientInitialize(ServerCommand):
    __game: BaseGame
    
    def __init__(self, server_network: BaseNetwork, game: BaseGame):
        super().__init__(server_network)
        
        self.__game = game
    
    def sync_all_objects(self, client_data: dict, socket: Socket):
        game_objects = self.__game.sprites()
        
        for game_object in game_objects:
            if not isinstance(game_object, NetworkObject):
                continue
            
            data = {
                "id": game_object.id,
                "name": game_object.__class__.__name__,
                "sync_data": game_object.get_data_to_sync(),
            }
            
            message = MessageProtocol.encode(SPAWN_OBJECT, client_data, data, True)
            
            socket.send(message)
    
    def execute(self, message_protocol: MessageProtocol, socket: Socket):
        self.sync_all_objects(message_protocol.client, socket)

class SyncObjectWithServer(ServerCommand):
    __game: BaseGame
    
    def __init__(self, server_network: BaseNetwork, game: BaseGame):
        super().__init__(server_network)
        
        self.__game = game
    
    def execute(self, message_protocol: MessageProtocol, socket: Socket):
        game_objects: list[GameObject] = self.__game.sprites()
        
        data = message_protocol.data
        id = data.get("id")
        sync_data = data.get("sync_data")
        
        if id is None or sync_data is None:
            return 
        
        for game_object in game_objects:
            if not isinstance(game_object, NetworkObject):
                continue
            
            if game_object.id != id:
                continue
            
            game_object.sync_data(sync_data)

# Client

class SpawnObject(ClientCommand):
    __game: BaseGame
    
    def __init__(self, client_network: BaseNetwork, game: BaseGame):
        super().__init__(client_network)

        self.__game = game
        
    
    def execute(self, message_protocol: MessageProtocol, *args):
        data = message_protocol.data
        id = data.get("id") 
        name = data.get("name")
        sync_data = data.get("sync_data")
        
        if id is None or name is None or sync_data is None:
            return
        
        cls = NETWORK_CLASSES.get(name)
        if cls is None:
            return

        game_object: NetworkObject = cls(id=id, is_proxy=False)
        game_object.sync_data(sync_data)
        
        self.__game.spawn(game_object)

class NetworkManager(GameObject):
    __network: BaseNetwork
    
    def __init__(self, id: str = None):
        super().__init__(id)
        
        if "--server" in argv:
            self.__network = ServerNetwork("127.0.0.1", 50000)
        else:
            self.__network = ClientNetwork("127.0.0.1", 50000)
        
        Network.set(self.__network)

        self.__network.start()
    
    def start(self):        
        self.image = Surface((32, 32))
        self.rect = self.image.get_rect()

        self._layer = -1
        
        if self.__network.is_server():
            self.__network.register(ON_CLINET_INITIALIZE, OnClientInitialize(self.__network, self.game))
            self.__network.register(SYNC_OBJECT, SyncObjectWithServer(self.__network, self.game))

            player = Player()
            player.setup_properties(position=(200, 100))
            self.spawn(player)
        
        if self.__network.is_client():
            self.__network.register(SPAWN_OBJECT, SpawnObject(self.__network, self.game))
    
    def update(self):
        ...
    
    def stop(self):
        self.__network.stop()
