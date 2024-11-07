from socket import socket as Socket
from sys import argv
from pygame import Surface

from game.game_object import GameObject
from game.base_game import BaseGame

from networking import BaseNetwork, ServerNetwork, ClientNetwork, Network, ProxyNetwork
from networking.network_commands import ClientCommand, ServerCommand
from networking.network_keys import *
from utils import Time

from protocol import MessageProtocol

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
            
            message = MessageProtocol.encode(SPAWN_OBJECT, {}, data, True)
            
            socket.send(message)
    
    def create_player(self, client_data: dict):
        client = self._server_network.get_client(client_data.get("id"))
        if client is None:
            return
        
        player = Player(client=client)
        
        player.setup_properties(position=(100, 100))
        self.__game.spawn(player)
        
        data = {
            "id": player.id,
            "name": player.__class__.__name__,
            "sync_data": player.get_data_to_sync()
        }
        
        self._server_network.broadcast(SPAWN_OBJECT, data, client_data)
        
    
    def execute(self, message_protocol: MessageProtocol, socket: Socket):
        client_data = message_protocol.client
        
        self.sync_all_objects(client_data, socket)
        self.create_player(client_data)


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
        
        client_id = "BOT" if message_protocol.client is None else message_protocol.client.get("id")
        
        client = self._server_network.get_client(client_id)
        
        if id is None or sync_data is None or client is None:
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
        client_data = message_protocol.client
        
        if id is None or name is None or sync_data is None:
            return
        
        cls = NETWORK_CLASSES.get(name)
        if cls is None:
            return

        is_proxy = True
        if client_data is not None:
            is_proxy = not self._network.client.id == client_data.get("id")

        game_object: NetworkObject = cls(id=id, is_proxy=is_proxy)
        game_object.sync_data(sync_data)
        
        self.__game.spawn(game_object)


class SyncObjectOnClient(ClientCommand):
    __game: BaseGame
    
    def __init__(self, client_network: BaseNetwork, game: BaseGame):
        super().__init__(client_network)
        
        self.__game = game
    
    def execute(self, message_protocol: MessageProtocol, *args):
        data = message_protocol.data
        id = data.get("id")
        sync_data = data.get("sync_data")
        
        if id is None or sync_data is None:
            return
        
        game_objects = self.__game.sprites()
        
        for game_object in game_objects:
            if not isinstance(game_object, NetworkObject):
                continue
            
            if game_object.id != id:
                continue
            
            game_object.sync_data(sync_data)


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
<<<<<<< HEAD
<<<<<<< HEAD
            self.__network.register(SYNC_OBJECT, SyncObjectWithServer(self.__network, self.game), False)
=======
            self.__network.register(SYNC_OBJECT, SyncObjectWithServer(self.__network, self.game))
>>>>>>> parent of f52e536 (Started adding udp to network)
            bot = Player()
        
            bot.set_bot(True)
            bot.setup_properties(position=(500, 100))
            self.game.spawn(bot)
=======
            self.__network.register(SYNC_OBJECT, SyncObjectWithServer(self.__network, self.game))
>>>>>>> parent of 2576ddc (update)
        
        if self.__network.is_client():
            self.__network.register(SPAWN_OBJECT, SpawnObject(self.__network, self.game))
            self.__network.register(SYNC_OBJECT, SyncObjectOnClient(self.__network, self.game))
        
        bot = Player()
        
        bot.set_bot(True)
        self.game.spawn(bot)
        
    
    def sync_data_between_clients(self):
        if not self.__network.is_server():
            return
        
        game_objects = self.game.sprites()
        
        for game_object in game_objects:
            if not isinstance(game_object, NetworkObject):
                continue
            
            client = game_object.client
            client_data = {"name": "Swanchick", "id": "BOT"}
            if client is not None:
                client_data = client.data
            
            sync_data = game_object.get_data_to_sync()
            if sync_data is None:
                continue
            
            data = {
                "id": game_object.id,
                "name": game_object.__class__.__name__,
                "owner_id": client_data["id"],
                "sync_data": sync_data
            }
            
            self.__network.broadcast(SYNC_OBJECT, data, client_data, True)
    
    def update(self):
        self.sync_data_between_clients()
    
    def stop(self):
        self.__network.stop()
