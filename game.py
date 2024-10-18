from pygame.display import (
    set_mode as display_set_mode, 
    set_caption as display_set_caption,
    flip as display_flip
)

from pygame.event import get as pygame_event_get
from pygame.time import Clock
from pygame import Surface, init as pygame_init
from pygame import QUIT

from colors import *

class Game:
    __res: tuple[int, int]
    __title: str
    __max_fps: int
    __display: Surface

    __game_run: bool
    __clock: Clock

    def __init__(self, res: tuple[int, int], title: str, max_fps=60):
        self.__res = res
        self.__title = title
        self.__max_fps = max_fps
        self.__game_run = True
        self.__clock = Clock()
        
        pygame_init()
        self.__display = display_set_mode(self.__res)
        display_set_caption(self.__title)

    def __update(self):
        pass

    def __draw(self):
        pass

    def start(self):
        while self.__game_run:
            for event in pygame_event_get():
                if event.type == QUIT:
                    self.__game_run = False

            self.__display.fill(WHITE)



            display_flip()
            self.__clock.tick(self.__max_fps)

            
        