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
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    SRCALPHA,
    init as pygame_init, 
    quit as pygame_quit
)
from pygame.transform import scale as pygame_scale

from pygame.draw import rect as pyg_rect

from utils.colors import *
from utils import Time, Vector
from game.game import Game
from game import LevelBuilder, UI
from utils import Global

from .base_window import BaseWindow

class Window(BaseWindow):
    __res: Vector
    __title: str
    __max_fps: int
    __display: Surface

    __current_scale: Vector

    __game_surface: Surface
    __level_surface: Surface
    __ui_surface: Surface
    
    __level_builder: LevelBuilder
    __level_pos: Vector
    __level_size: Vector

    __window_run: bool
    __clock: Clock

    __game: Game
    __ui: UI

    def __init__(self, res: Vector, title: str, max_fps=60):
        self.__res = res
        self.__title = title
        self.__max_fps = max_fps
        self.__window_run = True
        self.__clock = Clock()

        self.__current_scale = Vector.one()
        
        pygame_init()
        self.__display = display_set_mode(tuple(self.__res))
        self.__game_surface = Surface(tuple(self.__res))
        self.__ui_surface = Surface(tuple(self.__res), SRCALPHA)
        self.__level_size = Vector(1000, 1000)
        self.__level_surface = Surface(tuple(self.__level_size))
        self.__level_pos = Vector(0, 0)
        self.__game = Game(self)
        self.__ui = UI()
        
        Global.set("resolution", self.__res)
        
        display_set_caption(self.__title)

    def set_level_size(self, size: Vector):
        self.__level_surface = Surface(tuple(size))
    
    def set_camera_pos(self, pos: Vector):
        visible_width = self.__res.x // self.__current_scale.x
        visible_height = self.__res.y // self.__current_scale.y

        pos.set_x(max(min(0, pos.x), -(self.__level_size.x - visible_width)))
        pos.set_y(max(min(0, pos.y), -(self.__level_size.y - visible_height)))

        self.__level_pos = pos

    def set_camera_scale(self, scale: Vector):
        self.__current_scale = scale
        new_camera_res = (self.__res.x // scale.x, self.__res.y // scale.y)
        self.__game_surface = Surface(new_camera_res)
    
    def get_camera_pos(self) -> Vector:
        return self.__level_pos    
    
    def get_camera_scale(self):
        return self.__current_scale
    
    def start(self):
        self.__level_builder = LevelBuilder("test.lev")
        self.__level_builder.build(self.__game, self.__ui)
        self.__game.start()
        self.__ui.start()

        try:
            while self.__window_run:
                for event in pygame_event_get():
                    if event.type == QUIT:
                        self.__window_run = False
                    
                    if event.type == MOUSEBUTTONDOWN:
                        self.__ui.mouse_button_down()
                    elif event.type == MOUSEBUTTONUP:
                        self.__ui.mouse_button_up()
                
                Time.delta = self.__clock.tick(self.__max_fps) / 1000.0
                Time.cur_time += Time.delta
                
                self.__game.update()
                self.__ui.update()

                scaled_surface = pygame_scale(self.__game_surface, tuple(self.__res))
                self.__display.fill(BLACK)
                self.__display.blit(scaled_surface, (0, 0))

                self.__game_surface.fill(BLACK)
                self.__game_surface.blit(self.__level_surface, tuple(self.__level_pos))
                self.__level_surface.fill(WHITE)
                self.__game.draw(self.__level_surface)
                self.__game.draw_debug(self.__level_surface)

                self.__display.blit(self.__ui_surface, (0, 0))
                self.__ui.draw(self.__ui_surface)

                display_set_caption(str(self.__clock.get_fps()))

                display_flip()
        except KeyboardInterrupt:
            ...
        finally:
            self.__game.stop()
            pygame_quit()
