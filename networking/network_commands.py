from socket import socket as Socket

from protocol import Command, MessageProtocol 
from .base_network import BaseNetwork


class ClientCommand(Command):
    _network: BaseNetwork
    
    def __init__(self, client_network: BaseNetwork):
        self._network = client_network
    
    def execute(self, message_protocol: MessageProtocol, *args):
        ...


class ServerCommand(Command):
    _server_network: BaseNetwork
    
    def __init__(self, server_network: BaseNetwork):
        self._server_network = server_network
    
    def execute(self, message_protocol: MessageProtocol, socket: Socket):
        ...
