from socket import socket as Socket, timeout as SocketTimeout
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from .network import BaseNetwork
from .client import Client
from .network_keys import *

from json import loads as json_loads

from time import sleep as time_sleep



class ServerNetwork(BaseNetwork):
    __port: int
    __host: str
    __sock: Socket
    __server_run: bool
    __accept_clients_thread: Thread
    __clients: list[Client]
    __client_handlers: list[Thread]
    
    def __init__(self, host: str, port: int):
        self.__host = host
        self.__port = port
        self.__clients = []
        self.__client_handlers = []
    
    def init_server(self):
        self.__sock = Socket(AF_INET, SOCK_STREAM)
        
        self.__sock.bind((self.__host, self.__port))

        self.__server_run = True

    def start(self):
        if not self.__server_run:
            raise Exception("Server is not initialised!")
        
        self.__sock.listen()

        self.__accept_clients_thread = Thread(target=self.__accept_handler)
        self.__accept_clients_thread.start()

        try:
            while self.__server_run:
                time_sleep(1)
        except KeyboardInterrupt:
            self.stop()

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

    def __on_client_connected(self, socket: Socket, data: dict):
        client_data = data["client"]

        client = Client(socket, client_data["name"], client_data["id"])

        self.__clients.append(client)
    
    def __on_client_dissconnected(self, data: dict):
        pass

    def __handle_clients(self, client_socket: Socket):
        try:
            while self.__server_run:
                try:
                    data_receive = client_socket.recv(1024).decode("utf-8")
                    
                    if not data_receive:
                        break
                    
                    data = json_loads(data_receive)
                    action = data.get("action")

                    if action == CLIENT_CONNECTED:
                        self.__on_client_connected(client_socket, data)
                    elif action == CLIENT_DISCONNECTED:
                        self.__on_client_dissconnected(client_socket, data)

                    print(f"Received: {data}")
                except (OSError, SocketTimeout):
                    break

        except Exception as e:
            print(f"Error handling client: {e}")

        finally:            
            client_socket.close()
            print("Client connection closed.")
    
    def send(self):
        ...

    def is_server(self) -> bool:
        return True

    def is_client(self) -> bool:
        return False
    
    def is_proxy(self):
        return False
