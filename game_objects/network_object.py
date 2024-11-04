from game.game_object import GameObject
from networking import BaseNetwork, ProxyNetwork, Network

from networking.network_keys import *

NETWORK_CLASSES = {}


class NetworkObject(GameObject):
    _network: BaseNetwork
    
    def __init__(self, id = None, is_proxy: bool = False):
        super().__init__(id)
        
        if is_proxy:
            self._network = ProxyNetwork("Test")
        else:
            self._network = Network.get()
    
    def get_data_to_sync(self) -> dict:
        ...
    
    def sync_data(self, data: dict):
        ...
    
    def update(self):
        if not self._network.is_client():
            return
        
        data = {
            "id": self.id,
            "sync_data": self.get_data_to_sync()
        }
        
        self._network.send(SYNC_OBJECT, data)
    
    def is_server(self):
        return self._network.is_server()
    
    def is_client(self):
        return self._network.is_client()
    
    def is_proxy(self):
        return self._network.is_proxy()