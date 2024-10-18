from socket import socket as Socket, timeout as SocketTimeout
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from signal import signal, SIGINT
from time import sleep as time_sleep

class ServerNetwork:
    __port: int
    __host: str
    __sock: Socket
    __server_run: bool
    __accept_clients_thread: Thread
    __clients: list[Socket]
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
        
        print(f"Starting server on {self.__host}:{self.__port}.")
        
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

                self.__clients.append(client)

                print(client)
                print(f"Client ({address}) have been accepted.")

                handle_clients_thread = Thread(target=self.__handle_clients, args=(client, ))
                self.__client_handlers.append(handle_clients_thread)
                handle_clients_thread.start()

            except OSError:
                break

    def __handle_clients(self, client: Socket):
        try:
            while self.__server_run:
                try:
                    data = client.recv(1024)
                    if not data:
                        break

                    print(f"Received: {data.decode('utf-8')}")
                except (OSError, SocketTimeout):
                    break

        except Exception as e:
            print(f"Error handling client: {e}")

        finally:
            if client in self.__clients:
                self.__clients.remove(client)
            client.close()
            print("Client connection closed.")


