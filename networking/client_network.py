from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
from socket import timeout as SocketTimeOut
from threading import Thread

from protocol import MessageProtocol, ProtocolType

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
    __sock_tcp: Socket
    __client_run: bool
    __server_handler_tcp: Thread
    __server_handler_udp: Thread
    __client: Client

    def __init__(self, host: str, port: int):
        super().__init__()
        self.__host = host
        self.__port = port
        self.__client_run = False
        self.__client = None
        
        self.__sock_tcp = Socket(AF_INET, SOCK_STREAM)
        self.__sock_udp = Socket(AF_INET, SOCK_DGRAM)
        
        self.__server_handler_tcp = Thread(target=self.__handle_server_tcp)
        self.__server_handler_udp = Thread(target=self.__handle_server_udp)
        
        self._message_handler.register(ON_CLIENT_CONNECTED, OnClientInitialized(self))
    
    def start(self):
        self.__client_run = True
        
        self.__sock_tcp.connect((self.__host, self.__port))
        
        self.__server_handler_tcp.start()
        self.__server_handler_udp.start()
    
    def __handle_server_tcp(self):
        self.send(ON_CLIENT_CONNECTED, {"client_name": "Swanchick"})
        
        while self.__client_run:
            try:
                received_data = self.__sock_tcp.recv(2048)
                
                data: MessageProtocol = MessageProtocol.decode(received_data)
                
                if data is None:
                    break
                
                self._message_handler.handle(data, ProtocolType.TCP)
            except OSError:
                break

    def __handle_server_udp(self):
        while self.__client_run:
            try:
                received_data, server_address = self.__sock_tcp.recvfrom(2048)
                
                data: MessageProtocol = MessageProtocol.decode(received_data)
                
                if data is None:
                    break
                
                # self._message_handler.handle(data, ProtocolType.UDP)
            except OSError:
                break
    
    def send(self, action: str, data: dict = {}):
        if not self.__client_run:
            return

        client_data = None
        if self.client is not None:
            client_data = self.client.data
        
        data = MessageProtocol.encode(action, client_data, data)

        self.__sock_tcp.send(data)

    def stop(self):
        print("Stopping client...")

        self.send(ON_CLIENT_DISCONNECTED)
        
        self.__client_run = False

        self.__sock_tcp.close()

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