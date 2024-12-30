from socket import socket as Socket

from networking.network_commands import ServerCommand
from networking.network_keys import *
from networking import BaseNetwork
from protocol import MessageProtocol
from game.base_game import BaseGame
from game.game_object import GameObject

from .network_object import NetworkObject, NETWORK_CLASSES

from ..player import Player

class OnClientInitialize(ServerCommand):
    __game: BaseGame
    
    def __init__(self, server_network: BaseNetwork, game: BaseGame):
        super().__init__(server_network)
        
        self.__game = game
    
    def sync_all_objects(self, client_data: dict, socket: Socket):
        game_objects = self.__game.gameobjects
        
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
        game_objects: list[GameObject] = self.__game.gameobjects
        
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


class PlayerDisconnect(ServerCommand):
    __game: BaseGame
    
    def __init__(self, server_network: BaseNetwork, game: BaseGame):
        super().__init__(server_network)
        
        self.__game = game
            
    def execute(self, message_protocol: MessageProtocol, socket: Socket):
        client_data = message_protocol.client
        
        for game_object in self.__game.gameobjects:
            
            if not isinstance(game_object, NetworkObject):
                continue

            client = game_object.client
            
            if client.id == client_data["id"]:
                self.__game.remove(game_object)
                self._server_network.broadcast(REMOVE_OBJECT, {"game_object_id": game_object.id}, client_data, True)

class RequestToSpawnObjet(ServerCommand):
    __game: BaseGame
    
    def __init__(self, server_network: BaseNetwork, game: BaseGame):
        super().__init__(server_network)
        
        self.__game = game
    
    def execute(self, message_protocol, socket):
        ...