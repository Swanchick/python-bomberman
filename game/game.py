from pygame.display import (
    set_mode as display_set_mode, 
    set_caption as display_set_caption,
    flip as display_flip
)

from pygame.event import get as pygame_event_get
from pygame.time import Clock
from pygame import (
    Surface, 
    QUIT,
    init as pygame_init, 
    quit as pygame_quit
)

from utils.colors import *

from .game_object_manager import GameObjectManager

from game_objects.test_object import TestObject


class Game:
    __res: tuple[int, int]
    __title: str
    __max_fps: int
    __display: Surface

    __game_surface: Surface

    __game_run: bool
    __clock: Clock

    __game_object_manager: GameObjectManager

    def __init__(self, res: tuple[int, int], title: str, max_fps=60):
        self.__res = res
        self.__title = title
        self.__max_fps = max_fps
        self.__game_run = True
        self.__clock = Clock()
        
        pygame_init()
        self.__display = display_set_mode(self.__res)
        self.__game_surface = Surface(self.__res)
        
        display_set_caption(self.__title)

    def start(self):
        self.__game_object_manager = GameObjectManager()
        test_object = TestObject()
        self.__game_object_manager.add(test_object)


        while self.__game_run:
            for event in pygame_event_get():
                if event.type == QUIT:
                    self.__game_run = False

            self.__game_object_manager.update()

            self.__display.fill(WHITE)
            self.__display.blit(self.__game_surface, (0, 0))
            self.__game_surface.fill(WHITE)

            self.__game_object_manager.draw(self.__game_surface)

            display_flip()
            self.__clock.tick(self.__max_fps)
        
        pygame_quit()

            
        