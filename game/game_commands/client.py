from networking.client import Client
from networking import ClientCommand, BaseNetwork
from protocol import MessageProtocol

from ..game_object_network import GameObjectNetwork


class SpawnObjectOnClient(ClientCommand):
    def __init__(self, client_network: BaseNetwork, game):
        super().__init__(client_network)
        
        self.__game = game
    
    def execute(self, message_protocol: MessageProtocol, *args):
        data = message_protocol.data
        client_data = message_protocol.client
        client = Client(None, client_data["name"], client_data["id"])
        go_name = data["gameobject_name"]
        go_id = data["gameobject_id"]
        
        cls = GameObjectNetwork.get(go_name)
        
        gameobject = cls(go_id, client.id != self._network.client.id)
        
        self.__game.spawn(gameobject, client)


class OnSyncObject(ClientCommand):
    def __init__(self, client_network: BaseNetwork, game):
        super().__init__(client_network)
        
        self.__game = game
    
    def execute(self, message_protocol: MessageProtocol, *args):
        data = message_protocol.data
        
        for gameobject_data in data["gameobjects"]:
            name = gameobject_data["name"]
            gameobject_id = gameobject_data["gameobject_id"]
            gamecls = GameObjectNetwork.get(name)
            if gamecls is None:
                continue
                
            gameobject = gamecls(id=gameobject_id)
        