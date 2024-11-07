from abc import ABC
from socket import socket as Socket
from enum import Enum

from .message_protocol import MessageProtocol


class ProtocolType(Enum):
    TCP = 1
    UDP = 2


class Command(ABC):    
    def execute(self, message_protocol: MessageProtocol, *args):
        ...


class MessageHandler:
    __commands: dict[str, Command]

    def __init__(self):
        self.__commands = {}

    def register(self, action: str, command: Command, protocol_type: ProtocolType = ProtocolType.TCP):
        register = self.__commands.get(action)
        if register is None:
            self.__commands[action] = {}
        
        self.__commands[action][protocol_type] = command
    
    def handle(self, message_protocol: MessageProtocol, protocol_type: ProtocolType, *args):
        action = message_protocol.action
        
        register: dict[ProtocolType, Command] = self.__commands.get(action)
        if register is None:
            print(f"Unable to handle message \"{action}\"")
            return
        
        command: Command = register.get(protocol_type)
        if command is None:
            return

        command.execute(message_protocol, *args)
