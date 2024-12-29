from networking.network_commands import ClientCommand

from networking import BaseNetwork
from protocol import MessageProtocol
from game.base_game import BaseGame

from .network_object import NetworkObject, NETWORK_CLASSES


class SpawnObject(ClientCommand):
    __game: BaseGame
    
    def __init__(self, client_network: BaseNetwork, game: BaseGame):
        super().__init__(client_network)

        self.__game = game
    
    def spawn_object(self, client_data, id, name, sync_data):
        cls = NETWORK_CLASSES.get(name)
        if cls is None:
            return
        
        is_proxy = True
        if client_data is not None:
            is_proxy = not self._network.client.id == client_data.get("id")
        
        game_object: NetworkObject = cls(id=id, is_proxy=is_proxy)
        game_object.sync_data(sync_data)
        
        self.__game.spawn(game_object)
    
    def execute(self, message_protocol: MessageProtocol, *args):
        data = message_protocol.data
        id = data.get("id") 
        name = data.get("name")
        sync_data = data.get("sync_data")
        client_data = message_protocol.client
        
        if id is None or name is None or sync_data is None:
            return
        
        self.spawn_object(client_data, id, name, sync_data)


class SyncObjectOnClient(ClientCommand):
    __game: BaseGame
    
    def __init__(self, client_network: BaseNetwork, game: BaseGame):
        super().__init__(client_network)
        
        self.__game = game
    
    def sync_objects(self, id, sync_data):        
        for game_object in self.__game.gameobjects:
            if not isinstance(game_object, NetworkObject):
                continue
            
            if game_object.id != id:
                continue
            
            game_object.sync_data(sync_data)
    
    def execute(self, message_protocol: MessageProtocol, *args):
        data = message_protocol.data
        id = data.get("id")
        sync_data = data.get("sync_data")
        
        if id is None or sync_data is None:
            return
        
        self.sync_objects(id, sync_data)


class RemoveObject(ClientCommand):
    __game: BaseGame
    
    def __init__(self, client_network: BaseNetwork, game: BaseGame):
        super().__init__(client_network)
        
        self.__game = game
    
    def remove_object(self, game_object_id):
        for game_object in self.__game.gameobjects:
            if not isinstance(game_object, NetworkObject):
                continue
            
            if game_object.id == game_object_id:
                self.__game.remove(game_object)
                
                break
    
    def execute(self, message_protocol: MessageProtocol):
        data = message_protocol.data
        
        game_object_id = data.get("game_object_id")
        if game_object_id is None:
            return
        
        self.remove_object(game_object_id)