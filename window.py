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
from pygame.transform import scale as pygame_scale

from utils.colors import *
from utils import Time, Vector

from game.game import Game

class Window:
    __res: Vector
    __title: str
    __max_fps: int
    __display: Surface

    __game_surface: Surface
    __level_surface: Surface

    __window_run: bool
    __clock: Clock

    __game: Game
    
    __test: bool

    def __init__(self, res: Vector, title: str, max_fps=60):
        self.__res = res
        self.__title = title
        self.__max_fps = max_fps
        self.__window_run = True
        self.__clock = Clock()
        self.__test = True
        
        pygame_init()
        self.__display = display_set_mode(tuple(self.__res))
        self.__game_surface = Surface(tuple(self.__res))
        self.__level_surface = Surface(tuple(self.__res))
        self.__game = Game()
        
        display_set_caption(self.__title)

    def resize_game_surface(self, scale: Vector):
        new_camera_res = (self.__res.x // scale.x, self.__res.y // scale.y)
        self.__game_surface = Surface(new_camera_res)
    
    def start(self):
        self.__game.start()
        
        try:
            while self.__window_run:
                for event in pygame_event_get():
                    if event.type == QUIT:
                        self.__window_run = False
                
                Time.delta = self.__clock.tick(self.__max_fps) / 1000.0
                Time.cur_time += Time.delta
                
                # if Time.cur_time >= 2 and self.__test:
                #     self.resize_game_surface(Vector(5, 5))
                    
                #     self.__test = False
    
                
                self.__game.update()

                self.__display.fill(WHITE)
                
                scaled_surface = pygame_scale(self.__game_surface, tuple(self.__res))
                self.__display.blit(scaled_surface, tuple(Vector.zero()))
                
                self.__game_surface.blit(self.__level_surface, tuple(Vector.zero()))
                self.__level_surface.fill(WHITE)
                self.__game.draw(self.__level_surface)

                display_flip()
        except KeyboardInterrupt:
            ...
        finally:
            self.__game.stop()
            pygame_quit()
