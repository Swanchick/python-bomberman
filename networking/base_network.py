from abc import ABC, abstractmethod
from typing import Callable
from .client import Client
from utils import Data
from protocol import MessageHandler, Command


class BaseNetwork(ABC):
    _message_handler: MessageHandler

    def __init__(self):
        super().__init__()

        self._message_handler = MessageHandler()

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
    
    def register(self, action: str, command: Command):
        self._message_handler.handle(action, command)

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
