from json import (
    dumps as json_dumps, 
    loads as json_loads,
    JSONDecodeError
)

from typing import Self, Optional


class MessageProtocol:
    __action: str
    __client: dict
    __data: dict
    __from_server: bool

    def __init__(self, action: str, client: dict, data: dict, from_server: bool):
        self.__action = action
        self.__client = client
        self.__data = data
        self.__from_server = from_server
    
    @staticmethod
    def encode(action: str, client = None, data: dict = {}, from_server: bool = False) -> bytes:
        data_to_send = {
            "action": action,
            "data" : data,
            "client": client.data,
            "from_server": from_server
        }

        data_json = json_dumps(data_to_send)
        
        return data_json.encode("utf-8")
    
    @staticmethod
    def decode(message: bytes) -> Optional[Self]:
        message_string = message.decode("utf-8") 

        try:
            message_data = json_loads(message_string)
        except JSONDecodeError:
            return None
        finally:
            message_protocol = MessageProtocol(message_data["action"], message_data["client"], message_data["data"], message_data["from_server"])

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
