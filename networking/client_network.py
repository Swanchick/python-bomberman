from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread

from protocol import MessageProtocol

from .base_network import BaseNetwork
from .client import Client
from .network_keys import *
from .network_commands import ClientCommand

class OnClientInitialized(ClientCommand):
    def execute(self, message_protocol: MessageProtocol):
        data = message_protocol.data
        name = data["client_name"]
        client_id = data["client_id"]
        
        client = Client(self._network.socket, name, client_id)
        self._network.set_client(client)
        
        self._network.send(ON_CLINET_INITIALIZE, {})


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

        self._message_handler.register(ON_CLIENT_CONNECTED, OnClientInitialized(self))
    
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
                if data is None:
                    break

                print(data)
                
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

    def set_client(self, client: Client):
        self.__client = client

    def is_server(self) -> bool:
        return False

    def is_client(self) -> bool:
        return True
    
    def is_proxy(self) -> bool:
        return False

    @property
    def client(self) -> Client:
        return self.__client