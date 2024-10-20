from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from .base_network import BaseNetwork
from .client import Client
from json import dumps as json_dumps
from utils import Data
from .network_keys import *

import time

class ProxyNetwork(BaseNetwork):
    __client: Client

    def __init__(self, client: Client):
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