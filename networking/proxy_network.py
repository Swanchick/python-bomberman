from .base_network import BaseNetwork
from .client import Client
from .network_keys import *


class ProxyNetwork(BaseNetwork):
    def __init__(self):
        super().__init__()

    def send(self, action: str, data: dict):
        ...

    def stop(self):
        ...
    
    def is_server(self) -> bool:
        return False

    def is_client(self) -> bool:
        return False
    
    def is_proxy(self) -> bool:
        return True

    def broadcast(self):
        ...

    @property
    def client(self) -> Client:
        return self.__client