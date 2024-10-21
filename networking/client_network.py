from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread

from .base_network import BaseNetwork
from .client import Client
from protocol import MessageHandler, MessageProtocol, Command

from utils import Data
from .network_keys import *

class ClientCommand(Command):
    __network: BaseNetwork
    
    def __init__(self) -> None:
        super().__init__()

class ClientNetwork(BaseNetwork):
    __host: str
    __port: int
    __sock: Socket
    __client_run: bool
    __server_handler: Thread
    __client: Client

    def __init__(self, host: str, port: int):
        super().__init__()
        self.__host = host
        self.__port = port
        self.__client_run = False
        self.__client = None
    
    def init_client(self):
        self.__sock = Socket(AF_INET, SOCK_STREAM)
        self.__client_run = True
    
    def start(self):
        if not self.__client_run:
            raise Exception("Client is not initialized!")
        
        self.__sock.connect((self.__host, self.__port))

        self.__server_handler = Thread(target=self.__handle_server)
        self.__server_handler.start()
    
    def __handle_server(self):
        self.send(ON_CLIENT_CONNECTED, {"client_name": "Swanchick"})
        
        while self.__client_run:
            try:
                received_data = self.__sock.recv(1024)
                print(received_data.decode("utf-8"))
                
                data: MessageProtocol = MessageProtocol.decode(received_data)
                print(data)
                
                if data is None:
                    continue
                
                self._message_handler.handle(data)
            except OSError:
                break

    def send(self, action: str, data: dict):
        if not self.__client_run:
            return
        
        data = MessageProtocol.encode(action, self.client, data)

        self.__sock.send(data)

    def stop(self):
        print("Stopping client...")

        self.__client_run = False

        self.__sock.close()

        if self.__server_handler.is_alive():
            self.__server_handler.join()

        print("Client is stopped!")
    
    def register(self, action, command):
        ...

    def is_server(self) -> bool:
        return False

    def is_client(self) -> bool:
        return True
    
    def is_proxy(self) -> bool:
        return False

    @property
    def client(self) -> Client:
        return self.__client