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

    def register(self, action: str, command: Command):
        self.__commands[action] = command
    
    def handle(self, message_protocol: MessageProtocol, *args):
        action = message_protocol.action
        
        command = self.__commands.get(action)
        if command is None:
            print(f"Unable to handle message \"{action}\"")
            return 
        
        command.execute(message_protocol, *args)
