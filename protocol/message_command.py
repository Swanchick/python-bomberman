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
        self.__commands[action] = (protocol_type, command)
    
    def handle(self, message_protocol: MessageProtocol, protocol_type: ProtocolType, *args):
        action = message_protocol.action
        
        protocol_type, command = self.__commands.get(action)
        
        if protocol_type != protocol_type:
            return
        
        if command is None:
            print(f"Unable to handle message \"{action}\"")
            return
        
        command.execute(message_protocol, *args)
