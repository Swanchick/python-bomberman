from sys import argv
from pygame import Surface

from game.game_object import GameObject
from game.level_builder import LevelBuilder

from networking import BaseNetwork, ServerNetwork, ClientNetwork, Network
from networking.network_keys import *
from protocol import ProtocolType

from .sv_commands import (
    OnClientInitialize, 
    PlayerDisconnect, 
    SyncObjectOnServer, 
    SpawnObjectOnServer
)
from .cl_commands import SpawnObject, SyncObjectOnClient, RemoveObject

from .network_object import NetworkObject


@LevelBuilder.register_object
class NetworkManager(GameObject):
    HOST = "127.0.0.1"
    PORT = 50000
    PORT_UDP = 50001
    
    __network: BaseNetwork
    
    def __init__(self, id: str = None):
        super().__init__(id)
        
        if "--server" in argv:
            self.__network = ServerNetwork(self.HOST, self.PORT, self.PORT_UDP)
        else:
            self.__network = ClientNetwork(self.HOST, self.PORT)
        
        Network.set(self.__network)

        self.__network.start()
    
    def start(self):
        if self.__network.is_server():
            self.__network.register(ON_CLINET_INITIALIZE, OnClientInitialize(self.__network, self.game))
            self.__network.register(PLAYER_DISCONNECT, PlayerDisconnect(self.__network, self.game))
            
            self.__network.register(SYNC_OBJECT, SyncObjectOnServer(self.__network, self.game), ProtocolType.UDP)
            self.__network.register(SPAWN_OBJECT, SpawnObjectOnServer(self.__network, self.game))
        
        if self.__network.is_client():
            self.__network.register(SYNC_OBJECT, SyncObjectOnClient(self.__network, self.game), ProtocolType.UDP)
            self.__network.register(SPAWN_OBJECT, SpawnObject(self.__network, self.game))
            self.__network.register(REMOVE_OBJECT, RemoveObject(self.__network, self.game))
            
    def sync_data_between_clients(self):
        if not self.__network.is_server():
            return
        
        game_objects = self.game.gameobjects
        
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
            
            self.__network.broadcast_udp(SYNC_OBJECT, data, client_data, True)
    
    def update(self):
        self.sync_data_between_clients()
    
    def stop(self):
        if self.__network.is_client():
            self.__network.send(PLAYER_DISCONNECT)
        
        self.__network.stop()
