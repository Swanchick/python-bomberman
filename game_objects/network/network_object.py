from game.game_object import GameObject
from networking import BaseNetwork, ProxyNetwork, Network
from networking.client import Client

from networking.network_keys import *

NETWORK_CLASSES = {}

def register_network_class(cls):
    NETWORK_CLASSES[cls.__name__] = cls
    return cls


class NetworkObject(GameObject):
    _network: BaseNetwork
    
    client: Client # Only server-side attribute
    
    def __init__(self, id = None, is_proxy: bool = False, client: Client = None):
        super().__init__(id)
        
        if is_proxy:
            self._network = ProxyNetwork("Test")
        else:
            self._network = Network.get()
        
        if self.is_server():
            self.client = client
    
    def spawn_network_object(self, id, name, sync_data):
        ...
    
    def get_data_to_sync(self) -> dict:
        ...
    
    def sync_data(self, data: dict):
        ...
    
    def update(self):
        if not self.is_client():
            return
        
        data = {
            "id": self.id,
            "sync_data": self.get_data_to_sync()
        }
        
        self._network.send_udp(SYNC_OBJECT, data)
    
    def is_server(self):
        if self._network is None:
            return False
        
        return self._network.is_server()
    
    def is_client(self):
        if self._network is None:
            return False
        
        return self._network.is_client()
    
    def is_proxy(self):
        if self._network is None:
            return False
        
        return self._network.is_proxy()