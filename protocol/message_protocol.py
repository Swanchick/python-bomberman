from json import (
    dumps as json_dumps, 
    loads as json_loads,
    JSONDecodeError
)

from typing import Optional


class MessageProtocol:
    __action: str
    __client: dict
    __data: dict
    __from_server: bool

    def __init__(self, action: str = None, client: dict = None, data: dict = None, from_server: bool = None):
        self.__action = action
        self.__client = client
        self.__data = data
        self.__from_server = from_server
    
    def __repr__(self) -> str:
        data = {
            "action": self.__action,
            "client": self.__client,
            "data" : self.__data,
            "from_server": self.__from_server
        }
        
        return str(data)
    
    @staticmethod
    def encode(action: str = None, client = None, data: dict = {}, from_server: bool = False) -> bytes:
        client_data = None
        
        if client is not None:
            client_data = client
        
        data_to_send = {
            "action": action,
            "client": client_data,
            "data" : data,
            "from_server": from_server
        }

        data_json = json_dumps(data_to_send)
        
        return data_json.encode("utf-8")
    
    @staticmethod
    def decode(message: bytes):
        message_string = message.decode("utf-8") 

        message_data = {}
        
        try:
            message_data = json_loads(message_string)
        except JSONDecodeError:
            return None
        
        message_protocol = MessageProtocol(message_data.get("action"), message_data.get("client"), message_data.get("data"), message_data.get("from_server"))

        return message_protocol         
            

    @property
    def action(self) -> str:
        return self.__action
    
    @property
    def client(self) -> dict:
        return self.__client
    
    @property
    def data(self) -> dict:
        return self.__data
    
    @property
    def from_server(self) -> bool:
        return self.__from_server
