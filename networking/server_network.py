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
        client = Client(socket, data["client_name"], self._server_network)
        self._server_network.add_client(client)

        data = {
            "client_id": client.id, 
            "client_name": client.name,
            "port_udp": self._server_network.port_udp
        }

        send_data = MessageProtocol.encode(ON_CLIENT_CONNECTED, None, data, from_server=True)
        socket.send(send_data)
        

class OnClientConnectUDP(ServerCommand):
    def execute(self, message_protocol: MessageProtocol, client_address):
        client_data = message_protocol.client
        if client_data is None:
            return
        
        _, port = client_address

        print(client_address)
        client: Client = self._server_network.get_client(client_data["id"])
        client.set_port_udp(port)
        


class OnClientDisconnect(ServerCommand):
    def execute(self, message_protocol: MessageProtocol, socket: Socket):
        client = message_protocol.client

        self._server_network.remove_client(client["id"])


class ServerNetwork(BaseNetwork):
    __host: str
    __port_tcp: int
    __sock_tcp: Socket
    __sock_udp: Socket
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
        self.__sock_udp = Socket(AF_INET, SOCK_DGRAM)

        self._message_handler.register(ON_CLIENT_CONNECTED, OnClientConnect(self))
        self._message_handler.register(ON_CLIENT_DISCONNECTED, OnClientDisconnect(self))

        self._message_handler.register(ON_CLIENT_CONNECTED, OnClientConnectUDP(self), ProtocolType.UDP)
        
        self.__accept_clients_thread = Thread(target=self.__accept_handler)
        self.__client_handler_udp = Thread(target=self.__handle_clients_udp)

    def start(self):
        self.__server_run = True
        
        self.__sock_tcp.bind((self.__host, self.__port_tcp))
        self.__sock_tcp.listen(2)
        self.__sock_udp.bind((self.__host, self.__port_udp))
        
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
        self.__sock_udp.close()

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
                received_data = client_socket.recv(2048)
                if received_data is None:
                    break
                
                data: MessageProtocol = MessageProtocol.decode(received_data)
                if data is None:
                    continue
                
                self._message_handler.handle(data, ProtocolType.TCP, client_socket)
                
            except OSError:
                break
    
    def __handle_clients_udp(self):
        while self.__server_run:
            try:
                received_data, client_address = self.__sock_udp.recvfrom(2048)
                print(received_data.decode("utf-8"))
                
                if received_data is None:
                    break
                
                data: MessageProtocol = MessageProtocol.decode(received_data)
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
            
            client.send(action, data, client_out)
    
    def broadcast_udp(self, action: str, data: dict, client_out: dict = None, ignore: bool = False):
        for client in self.__clients:
            if client_out is not None:
                if client.id == client_out["id"] and ignore:
                    continue
            
            client.send_udp(action, data, client_out)

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
    def socket_udp(self) -> Socket:
        return self.__sock_udp

    @property
    def clients(self) -> list[Client]:
        return self.__clients

    @property
    def port_udp(self) -> int:
        return self.__port_udp
