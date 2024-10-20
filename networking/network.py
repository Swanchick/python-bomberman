from abc import ABC, abstractmethod
from typing import Callable
from .client import Client
from utils import Data

ON_CONNECT = "on_connect"
ON_RECEIVE = "on_receive"


class BaseNetwork(ABC):
    __registered_handlers: dict[str, Callable]

    def __init__(self):
        super().__init__()

        self.__registered_handlers = {}

    def _call(self, name: str, *args):
        func = self.__registered_handlers.get(name)
        if func is None:
            return
        
        func(*args)

    def register_on_connect(self, func: Callable):
        self.__registered_handlers[ON_CONNECT] = func

    def register_on_receive(self, func: Callable):
        self.__registered_handlers[ON_RECEIVE] = func

    def broadcast(self, action: str, data: Data, client_out: Client):
        ...

    def send(self, action: str, data: Data):
        ...

    @abstractmethod
    def stop(self):
        ...

    @abstractmethod
    def is_server(self) -> bool:
        ...
    
    @abstractmethod
    def is_client(self) -> bool:
        ...
    
    @abstractmethod
    def is_proxy(self) -> bool:
        ...

    @property
    def client(self) -> Client:
        return None
