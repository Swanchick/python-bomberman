from socket import socket as Socket
from uuid import uuid4
from typing import Optional

from protocol import MessageProtocol

from .base_client import BaseClient

class Client(BaseClient):    
    __sock: Socket
    __host: str
    
    __port_udp: int
    __id: str
    __name: str

    def __init__(self, sock: Socket, name: str, network, id: Optional[str] = None):
        self.__sock = sock
        self.__name = name
        self.__server_network = network
        self.__port_udp = 0
        
        if self.__sock is not None:
            self.__host, _ = self.__sock.getsockname()
        
        if id is None:
            self.__id = str(uuid4())
        else:
            self.__id = id

    def send(self, action: str, data: dict, client_sender: dict = None):        
        print(f"data sended: {data}")
        data = MessageProtocol.encode(action, client_sender, data, True)
        self.__sock.send(data)

    def send_udp(self, action: str, data: dict, client_sender: dict = None):
        if self.__port_udp == 0:
            return
        
        data = MessageProtocol.encode(action, client_sender, data, True)

        sock_udp: Socket = self.__server_network.socket_udp
        sock_udp.sendto(data, (self.__host, self.__port_udp))

    def close(self):
        self.__sock.close()

    def set_port_udp(self, port: int):
        self.__port_udp = port
    
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