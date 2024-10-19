from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from .network import BaseNetwork
from .client import Client
from json import dumps as json_dumps
from utils import Data
from .network_keys import *

import time

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
        
    
    def init_client(self):
        self.__sock = Socket(AF_INET, SOCK_STREAM)
        self.__client_run = True
    
    def start(self):
        if not self.__client_run:
            raise Exception("Client is not initialized!")
        
        self.__sock.connect((self.__host, self.__port))
        self.__client = Client(self.__sock, "Swanchick")

        self.__server_handler = Thread(target=self.__handle_server)
        self.__server_handler.start()

        self.send(CLIENT_CONNECTED, {})
    
    def __handle_server(self):
        while self.__client_run:
            try:
                data = self.__sock.recv(1024).decode("utf-8")
            except OSError:
                break

    def send(self, action: str, data: dict):
        if not self.__client_run:
            return

        data = {
            "action": action,
            "client": self.__client.data,
            "data": data
        }

        data_send = json_dumps(data)

        self.__sock.send(data_send.encode("utf-8"))

    def stop(self):
        print("Stopping client...")

        self.send("client-disconnected", {})

        self.__client_run = False

        self.__sock.close()

        if self.__server_handler.is_alive():
            self.__server_handler.join()

        print("Client is stopped!")
    
    def is_server(self) -> bool:
        return False

    def is_client(self) -> bool:
        return True
    
    def is_proxy(self) -> bool:
        return False

    def broadcast(self):
        ...

    @property
    def client(self) -> Client:
        return self.__client