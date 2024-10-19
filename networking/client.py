from socket import socket as Socket

class Client:
    __sock: Socket 
    __id: str
    __name: str

    def __init__(self, sock: Socket):
        self.__sock = sock

    def send(self, data: str):
        ...