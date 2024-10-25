class GameObjectNetwork:
    registered_network_objects: dict
    
    instance = None
    
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.registered_network_objects = {}

        return cls.instance

    def register_internal(self, cls):
        name = cls.__name__
        self.registered_network_objects[name] = cls

    def get_internal(self, name) -> dict:
        return self.registered_network_objects.get(name)

    @staticmethod
    def register(cls):
        gon = GameObjectNetwork()
        gon.register_internal(cls)
        
        return cls

    @staticmethod
    def get(name):
        gon = GameObjectNetwork()
        
        return gon.get_internal(name)
