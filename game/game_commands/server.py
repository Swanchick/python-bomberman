from socket import socket
from networking import ServerCommand
from networking.network_keys import *
from networking.base_network import BaseNetwork
from protocol.message_protocol import MessageProtocol



class OnRequestSyncObjects(ServerCommand):
    def __init__(self, server_network: BaseNetwork, game):
        super().__init__(server_network)
        self.__game = game
    
    def execute(self, message_protocol: MessageProtocol, socket: socket):
        gameobjects = self.__game.sprites()
        client_id = message_protocol.client.get("id")
        if client_id is None:
            return
        
        client = self._server_network.get_client(client_id)
        
        data = {
            "gameobjects": []
        }
        
        for gameobject in gameobjects:
            name = gameobject.__class__.__name__
            position = gameobject.position
            gameobject_id = gameobject.id
            
            if gameobject.owner is None:
                continue

            owner = gameobject.owner.data
            
            data["gameobjects"].append({
                "name": name,
                "position": position,
                "gameobject_id": gameobject_id,
                "owner": owner
            })
            
        client.send(REQUEST_SYNC_OBJECTS, data)
        