from json import (
    dumps as json_dumps, 
    loads as json_loads
)

from .base_game_object import BaseGameObject
from .base_game import BaseGame

class LevelBuilder:
    LEVEL_PATH: str = "res/levels/"
    registered_classes: dict = {}
    
    __level_name: str
    
    __width: int
    __height: int
    
    def __init__(self, level_name: str) -> None:
        self.__level_name = level_name
        
    def __open_file(self) -> dict:
        with open(self.LEVEL_PATH + self.__level_name, "r") as file:
            data = file.read()
            
            try:
                level_data = json_loads(data)
            except Exception as e:
                level_data = None
            finally:
                file.close()
                
                return level_data
    
    def build(self, game: BaseGame, ui: BaseGame):
        level_data = self.__open_file()
        if level_data is None:
            return
        
        settings = level_data.get("settings")
        if settings is None:
            return
        
        self.__width = settings.get("width")
        self.__height = settings.get("height")
        
        objects = level_data.get("objects")
        if objects is not None:
            for game_object_data in objects:
                class_name = game_object_data.get("class_name")
                if class_name is None:
                    continue
                
                game_object_cls = self.registered_classes.get(class_name)
                if game_object_cls is None:
                    continue
                
                properties = game_object_data.get("properties")
                if properties is None:
                    continue
                
                game_object = game_object_cls()
                game_object.setup_properties(**properties)
                game.spawn(game_object)
        
        panels = level_data.get("ui")
        if panels is not None:
            for panel_data in panels:
                class_name = panel_data.get("class_name")
                if class_name is None:
                    continue
                
                panel_cls = self.registered_classes.get(class_name)
                if panel_cls is None:
                    continue
                
                properties = panel_data.get("properties")
                if properties is None:
                    continue
                
                panel = panel_cls()
                panel.setup_properties(**properties)
                ui.spawn(panel)
    
    @property
    def width(self) -> int:
        return self.__width
    
    @property
    def height(self) -> int:
        return self.__height
    
    @classmethod
    def register_object(cls, game_object_cls: type) -> None:
        class_name = game_object_cls.__name__
        if class_name is not None:
            cls.registered_classes[class_name] = game_object_cls
            
        return game_object_cls
