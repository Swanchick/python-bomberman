from socket import socket as Socket
from uuid import uuid4
from typing import Optional
from .base_client import BaseClient
from protocol import MessageProtocol

class Client(BaseClient):
    __sock: Socket 
    __id: str
    __name: str
    __address: str
    __port_udp: int

    def __init__(self, sock: Socket, name: str, port_udp: int, id: Optional[str] = None):
        self.__sock = sock
        self.__name = name
        self.__port_udp = port_udp
        self.__address, _ = self.__sock.getsockname()

        if id is None:
            self.__id = str(uuid4())
        else:
            self.__id = id

    def send(self, action: str, data: dict, client_sender: dict = None):        
        data = MessageProtocol.encode(action, client_sender, data, True)
        self.__sock.send(data)
    
    def send_fast(self, socket_udp: Socket, action: str, data: dict, client_sender: dict = None):
        data = MessageProtocol.encode(action, client_sender, data, True)

        socket_udp.sendto(data, (self.__address, self.__port_udp))

    def close(self):
        self.__sock.close()

    @property
    def id(self) -> str:
        return self.__id
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def socket(self) -> Socket:
        return self.__sock
    
    @property
    def data(self) -> dict:
        client_info = {
            "id": self.__id,
            "name": self.__name
        }

        return client_info