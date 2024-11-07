from abc import ABC, abstractmethod
from socket import socket as Socket

from .client import Client
from protocol import MessageHandler, Command, ProtocolType


class BaseNetwork(ABC):
    _message_handler: MessageHandler

    def __init__(self):
        super().__init__()

        self._message_handler = MessageHandler()

    def setup_udp(self, port_udp: int):
        ...

    def broadcast(self, action: str, data: dict, client_out: dict, ignore: bool):
        ...

    def broadcast_udp(self, action: str, data: dict, client_out: dict, ignore: bool):
        ...

    def send(self, action: str, data: dict = {}):
        ...
    
    def send_udp(self, action: str, data: dict = {}):
        ...

    def add_client(self):
        ...

    def remove_client(self):
        ...
    
    def register(self, action: str, command: Command, protocol_type: ProtocolType = ProtocolType.TCP):
        self._message_handler.register(action, command, protocol_type)

    def set_client(self, client: Client):
        ...

    def get_client(self, client_id: str) -> Client:
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
    def socket(self) -> Socket:
        ...

    @property
    def socket_udp(self) -> Socket:
        ...

    @property
    def client(self) -> Client:
        ...

    @property
    def clients(self) -> list[Client]:
        ...
    
    @property
    def port_udp(self) -> int:
        ...
