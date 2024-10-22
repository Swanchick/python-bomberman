from typing import Self


class GameObjectNetwork:
    __registered_network_objects: dict
    
    instance: Self = None
    
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        
        cls.__registered_network_objects = {}

        return cls.instance

    def register_internal(self, cls):
        name = cls.__name__

        self.__registered_network_objects[name] = cls

    def get_internal(self, name) -> dict:
        return self.__registered_network_objects.get(name)

    @staticmethod
    def register(cls):
        gon = GameObjectNetwork()
        gon.register_internal(cls)
        
        return cls

    @staticmethod
    def get(name) -> dict:
        gon = GameObjectNetwork()

        return gon.get(name)
