from utils import resources, Vector
from json import loads as json_loads

class Settings:
    instance = None
    __res: tuple[int, int]
    
    __player_name: str

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        
        cls.load(cls)

        return cls.instance
    
    def load(self):
        with open(resources("game.json"), "r") as f:
            data = f.read()
            
            d: dict = json_loads(data)

            game_settings = d.get("game-settings")
            if game_settings is None:
                raise Exception("Settings file is incorrect!")
            
            width = game_settings.get("screen-width")
            if width is None:
                raise Exception("Width is required!")
            
            height = game_settings.get("screen-height")
            if height is None:
                raise Exception("Height is required!")

            self.__res = Vector(width, height)

            player_settings = d.get("player-settings")
            if player_settings is None:
                player_settings = {"name": "Swanchick"}
            
            self.__player_name = player_settings.get("name")

    @property
    def player_name_internal(self) -> str:
        return self.__player_name
    
    @property
    def res_internal(self) -> Vector:
        return self.__res

    @staticmethod
    def player_name():
        settings = Settings()
        
        return settings.player_name_internal
    
    @staticmethod
    def res() -> Vector:
        settings = Settings()

        return settings.res_internal
