from socket import socket as Socket, timeout as SocketTimeout
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from .base_network import BaseNetwork
from .client import Client
from .network_keys import *

from json import loads as json_loads

from time import sleep as time_sleep

from protocol import MessageHandler, Command, MessageProtocol 


class ServerCommand(Command):
    _server_network: BaseNetwork
    
    def __init__(self, server_network: BaseNetwork):
        self._server_network = server_network


class OnClientConnect(ServerCommand):
    def execute(self, message_protocol: MessageProtocol, socket: Socket):
        client = Client(socket, client["name"])

        self._server_network.add_client(client)

class OnClientDisconnect(ServerCommand):
    def execute(self, message_protocol: MessageProtocol, socket: Socket):
        client = message_protocol.client

        self._server_network.remove_client(client["id"])


class ServerNetwork(BaseNetwork):
    __port: int
    __host: str
    __sock: Socket
    __server_run: bool
    __accept_clients_thread: Thread
    __clients: list[Client]
    __client_handlers: list[Thread]
    
    def __init__(self, host: str, port: int):
        super().__init__()

        self.__host = host
        self.__port = port
        self.__clients = []
        self.__client_handlers = []
    
    def init_server(self):
        self.__sock = Socket(AF_INET, SOCK_STREAM)
        
        self.__sock.bind((self.__host, self.__port))
        self.__server_run = True

        self._message_handler.register(ON_CLIENT_CONNECTED, OnClientConnect(self))
        self._message_handler.register(ON_CLIENT_DISCONNECTED, OnClientDisconnect(self))

    def start(self):
        if not self.__server_run:
            raise Exception("Server is not initialised!")

        self.__sock.listen()

        self.__accept_clients_thread = Thread(target=self.__accept_handler)
        self.__accept_clients_thread.start()

        print("Server started")

    def stop(self):
        print("Stopping server...")

        self.__server_run = False

        for client in self.__clients:
            client.close()

        for handler in self.__client_handlers:
            if handler.is_alive():
                handler.join()

        self.__sock.close()

        if self.__accept_clients_thread.is_alive():
            self.__accept_clients_thread.join()
        
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
                client, address = self.__sock.accept()

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
        try:
            while self.__server_run:
                try:
                    data_receive = client_socket.recv(1024)
                    if not data_receive:
                        break
                    
                    data: MessageProtocol = MessageProtocol.decode(data_receive)
                    self.__message_handler.handle(data.action, client_socket, self)
                    
                except (OSError, SocketTimeout):
                    break

        except Exception as e:
            print(f"Error handling client: {e}")

        finally:            
            client_socket.close()
            print("Client connection closed.")
    
    def broadcast(self, action: str, data: dict, client_out: Client = None):
        for client in self.__clients:
            if client.id == client_out.id:
                continue

            client.send(action, data, client_out)
    
    def is_server(self) -> bool:
        return True

    def is_client(self) -> bool:
        return False
    
    def is_proxy(self) -> bool:
        return False

    @property
    def clients(self) -> list[Client]:
        return self.__clients
