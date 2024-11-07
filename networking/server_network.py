from socket import socket as Socket, timeout as SocketTimeout
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
from threading import Thread

from protocol import MessageProtocol, ProtocolType

from .base_network import BaseNetwork
from .client import Client
from .network_keys import *
from .network_commands import ServerCommand


class OnClientConnect(ServerCommand):
    def execute(self, message_protocol: MessageProtocol, socket: Socket):
        data = message_protocol.data
        client = Client(socket, data["client_name"])
        self._server_network.add_client(client)
        
        send_data = MessageProtocol.encode(ON_CLIENT_CONNECTED, None, {"client_id": client.id, "client_name": client.name}, from_server=True)
        socket.send(send_data)
        

class OnClientDisconnect(ServerCommand):
    def execute(self, message_protocol: MessageProtocol, socket: Socket):
        client = message_protocol.client

        self._server_network.remove_client(client["id"])


class ServerNetwork(BaseNetwork):
    __host: str
    __port_tcp: int
    __sock_tcp: Socket
    __socket_udp: Socket
    __server_run: bool
    __accept_clients_thread: Thread
    __clients: list[Client]
    __client_handlers: list[Thread]
    __client_handler_udp: Thread
    
    def __init__(self, host: str, port_tcp: int, port_udp: int):
        super().__init__()

        self.__host = host
        self.__port_tcp = port_tcp
        self.__port_udp = port_udp
        self.__clients = []
        self.__client_handlers = []

        self.__sock_tcp = Socket(AF_INET, SOCK_STREAM)
        self.__socket_udp = Socket(AF_INET, SOCK_DGRAM)

        self._message_handler.register(ON_CLIENT_CONNECTED, OnClientConnect(self))
        self._message_handler.register(ON_CLIENT_DISCONNECTED, OnClientDisconnect(self))
        
        self.__accept_clients_thread = Thread(target=self.__accept_handler)
        self.__client_handler_udp = Thread(target=self.__handle_clients_udp)

    def start(self):
        self.__server_run = True
        
        self.__sock_tcp.bind((self.__host, self.__port_tcp))
        self.__sock_tcp.listen(2)
        self.__socket_udp.bind((self.__host, self.__port_udp))
        
        self.__accept_clients_thread.start()
        self.__client_handler_udp.start()
        print("Server started")

    def stop(self):
        print("Stopping server...")

        self.__server_run = False

        for client in self.__clients:
            client.close()

        for handler in self.__client_handlers:
            if handler.is_alive():
                handler.join()

        self.__sock_tcp.close()
        self.__socket_udp.close()

        if self.__accept_clients_thread.is_alive():
            self.__accept_clients_thread.join()
        
        if self.__client_handler_udp.is_alive():
            self.__client_handler_udp.join()
        
        print("Server stopped.")

    def add_client(self, client: Client):
        self.__clients.append(client)

    def remove_client(self, id: str):
        for client in self.__clients:
            if client.id == id:
                self.__clients.remove(client)
                break

    def __accept_handler(self):
        while self.__server_run:
            try:
                client, address = self.__sock_tcp.accept()

                print(client)
                print(f"Client ({address}) have been accepted.")

                handle_clients_thread = Thread(target=self.__handle_clients, args=(client, ))
                self.__client_handlers.append(handle_clients_thread)
                handle_clients_thread.start()

            except OSError:
                break

    def get_client(self, id: str) -> Client:
        for client in self.__clients:
            if client.id == id:
                return client

    def __handle_clients(self, client_socket: Socket):
        while self.__server_run:
            try:
                data_receive = client_socket.recv(2048)
                if not data_receive:
                    break
                
                data: MessageProtocol = MessageProtocol.decode(data_receive)
                if data is None:
                    continue
                
                self._message_handler.handle(data, ProtocolType.TCP, client_socket)
                
            except OSError:
                break
    
    def __handle_clients_udp(self):
        while self.__server_run:
            try:
                data_receive, client_address = self.__socket_udp.recvfrom(2048)
                if not data_receive:
                    break
                
                data: MessageProtocol = MessageProtocol.decode(data_receive)
                if data is None:
                    continue
                
                self._message_handler.handle(data, ProtocolType.UDP, client_address)
                
            except OSError:
                break
    
    def send(self, action: str, data: dict, client_id: str, client_from: Client = None):
        for client in self.__clients:
            if client.id == client_id:
                client.send(action, data, client_from)

                break 

    def broadcast(self, action: str, data: dict, client_out: dict = None, ignore: bool = False):
        for client in self.__clients:
            if client_out is not None:
                if client.id == client_out["id"] and ignore:
                    continue
            
            socket = client.socket
            socket.send(MessageProtocol.encode(action, client_out, data, True))
            
    
    def get_client(self, client_id: str) -> Client:
        for client in self.__clients:
            if client.id == client_id:
                return client
    
    def is_server(self) -> bool:
        return True

    def is_client(self) -> bool:
        return False
    
    def is_proxy(self) -> bool:
        return False

    @property
    def clients(self) -> list[Client]:
        return self.__clients
