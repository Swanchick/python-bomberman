from game.ui.panel import Panel
from game.ui.text import Text
from game import LevelBuilder
from utils import Global, Vector

from .button import Button
from .label import Label


@LevelBuilder.register_object
class HUD(Panel):
    __button: Button
    
    __label: Label
    
    def start(self):
        res = Global.get("resolution", Vector(800, 600))
        
        self.__button = Button(Text(16, "Test Button", (0, 0, 0)), 200, 32)
        self.__button.position = Vector(0, res.y - self.__button.height)
        self.__button.register_click(self.press)
        self.game.spawn(self.__button)
        
        self.__label = Label(Text(16, "Test Label", (0, 0, 0)))
        self.__label.position = Vector(100, 200)
        self.game.spawn(self.__label)
        self.__label.start()
        
    
    def press(self):
        print("Hello World")