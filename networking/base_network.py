from abc import ABC, abstractmethod
from typing import Callable
from .client import Client
from utils import Data
from protocol import Command


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

    def broadcast(self, action: str, data: Data, client_out: Client):
        ...

    def send(self, data: dict):
        ...

    def add_client(self):
        ...

    def remove_client(self):
        ...

    @abstractmethod
    def register(self, action: str, command: Command):
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
        ...

    @property
    def clients(self) -> list[Client]:
        ...
