from abc import ABC
from .message_protocol import MessageProtocol
from socket import socket as Socket


class Command(ABC):    
    def execute(self, message_protocol: MessageProtocol, *args):
        ...


class MessageHandler:
    __commands: dict[str, Command]

    def __init__(self):
        self.__commands = {}

    def register(self, action: str, command: Command, udp: bool = False):
        self.__commands[action] = (udp, command)
    
    def handle(self, message_protocol: MessageProtocol, udp: bool, *args):
        action = message_protocol.action
        
        data = self.__commands.get(action)
        if data is None:
            print(f"Unable to handle message \"{action}\"")
            return 
        
        if data[0] != udp:
            return

        command: Command = data[1]
        command.execute(message_protocol, *args)
