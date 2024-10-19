from socket import socket as Socket
from uuid import uuid4
from typing import Optional

class Client:
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

    def send(self, data: str):        
        self.__sock.send(data.encode("utf-8"))

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