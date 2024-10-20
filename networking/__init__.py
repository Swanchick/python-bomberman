from .client_network import ClientNetwork
from .server_network import ServerNetwork
from .proxy_network import ProxyNetwork
from .network import BaseNetwork

class Network:
    instance = None
    __network: BaseNetwork

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        
        cls.set_internal(cls, None)

        return cls.instance
    
    def set_internal(self, network: BaseNetwork):
        self.__network = network

    @property
    def get_internal(self) -> BaseNetwork:
        return self.__network
    
    @staticmethod
    def get() -> BaseNetwork:
        net = Network()
        return net.get_internal
    
    @staticmethod
    def set(network: BaseNetwork):
        net = Network()
        net.set_internal(network)


from . import Network
