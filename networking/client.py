from socket import socket as Socket
from uuid import uuid4
from typing import Optional
from typing import Self
from .base_client import BaseClient
from protocol import MessageProtocol

class Client(BaseClient):
    __sock: Socket 
    __id: str
    __name: str

    def __init__(self, sock: Socket, name: str, id: Optional[str] = None):
        self.__sock = sock
        self.__name = name
        if id is None:
            self.__id = str(uuid4())
        else:
            self.__id = id

    def send(self, action: str, data: dict, client_sender: Self = None):       
        client_data = None
        if client_sender is not None:
            client_data = client_sender.data
        
        data = MessageProtocol.encode(action, client_data, data, True)
        self.__sock.send(data)

    def close(self):
        self.__sock.close()

    @property
    def id(self) -> str:
        return self.__id
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def data(self) -> dict:
        client_info = {
            "id": self.__id,
            "name": self.__name
        }

        return client_info