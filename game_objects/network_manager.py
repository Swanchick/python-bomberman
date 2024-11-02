from sys import argv
from pygame import Surface

from game.game_object import GameObject
from networking import BaseNetwork, ServerNetwork, ClientNetwork, Network


class NetworkManager(GameObject):
    __network: BaseNetwork
    
    def start(self):
        self.image = Surface((32, 32))
        self.rect = self.image.get_rect()

        self._layer = -1
        
        if "--server" in argv:
            self.__network = ServerNetwork("127.0.0.1", 50000)
        else:
            self.__network = ClientNetwork("127.0.0.1", 50000)
        
        Network.set(self.__network)

        self.__network.start()
    
    def update(self):
        ...
    
    def stop(self):
        self.__network.stop()


class NetworkObject(GameObject):
    _network: BaseNetwork
    
    def __init__(self, id = None):
        super().__init__(id)

        self._network = Network.get()
    
    def start(self):
        ...

    def update(self):
        ...
    
    def stop(self):
        ...
    
    @property
    def is_server(self):
        return self._network.is_server()
    
    @property
    def is_client(self):
        return self._network.is_client()
    
    @property
    def is_proxy(self):
        return self._network.is_proxy()
