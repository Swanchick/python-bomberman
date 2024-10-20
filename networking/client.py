from socket import socket as Socket
from uuid import uuid4
from typing import Optional
from json import dumps as json_dumps
from typing import Self
from .base_client import BaseClient

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
        data_dict = {
            "action": action,
            "data": data,
            "from_server": False
        }

        if client_sender is None:
            data_dict["from_server"] = True
        if client_sender is not None:
            data_dict["client"] = client_sender.data

        send_data = json_dumps(data_dict)

        self.__sock.send(send_data.encode("utf-8"))

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