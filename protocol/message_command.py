from abc import ABC


class Command(ABC):
    def execute(self, client: dict, data: dict, from_server: bool):
        ...

class MessageHandler:
    __commands: dict[str, Command]

    def __init__(self):
        self.__commands = {}

    def register(self, action: str, command: Command):
        self.__commands[action] = command
    
    def handle(self, action: str, client: dict, data: dict, from_server: bool):
        command = self.__commands.get(action)
        if command is None:
            print(f"Unable to handle message \"{action}\"")
            return 
        
        command.execute(client, data, from_server)
