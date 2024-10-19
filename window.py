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
from utils import Time, Vector

from game.game import Game

from game_objects.player import Player

class Window:
    __res: Vector
    __title: str
    __max_fps: int
    __display: Surface

    __game_surface: Surface

    __window_run: bool
    __clock: Clock

    __game: Game

    def __init__(self, res: Vector, title: str, max_fps=60):
        self.__res = res
        self.__title = title
        self.__max_fps = max_fps
        self.__window_run = True
        self.__clock = Clock()
        
        pygame_init()
        self.__display = display_set_mode(tuple(self.__res))
        self.__game_surface = Surface(tuple(self.__res))
        
        display_set_caption(self.__title)

    def start(self):
        self.__game = Game()
        test_object = Player()
        self.__game.add(test_object)
        try:
            while self.__window_run:
                Time.delta = self.__clock.tick(self.__max_fps) / 1000.0
                Time.cur_time += Time.delta

                for event in pygame_event_get():
                    if event.type == QUIT:
                        self.__window_run = False

                self.__game.update()

                self.__display.fill(WHITE)
                self.__display.blit(self.__game_surface, tuple(Vector.zero()))
                self.__game_surface.fill(WHITE)

                self.__game.draw(self.__game_surface)

                display_flip()
        except KeyboardInterrupt:
            pass
        finally:
            self.__game.stop()
            pygame_quit()
