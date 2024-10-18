from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import time

class ClientNetwork:
    __host: str
    __port: int
    __sock: Socket
    __client_run: bool
    __server_handler: Thread

    def __init__(self, host: str, port: int):
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

        self.__server_handler = Thread(target=self.__handle_server)
        self.__server_handler.start()

        self.send("Hello World")

        try:
            while self.__client_run:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def send(self, data: str):
        if not self.__client_run:
            return

        self.__sock.send(data.encode("utf-8"))

    def stop(self):
        print("Stopping client...")

        self.__client_run = False
        
        if self.__server_handler.is_alive():
            self.__server_handler.join()

        self.__sock.close()

        print("Client is stopped!")

    def __handle_server(self):
        while self.__client_run:
            try:
                data = self.__sock.recv(1024).decode('utf-8')
                print(data)
            except OSError:
                break
