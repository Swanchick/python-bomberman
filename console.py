from game.game import Game
from networking import Network
from pygame.time import Clock
from utils import Time

class Console:
    __game: Game
    __max_fps: int
    __clock: Clock

    __console_run: bool

    def __init__(self, max_fps: int = 60):
        self.__max_fps = max_fps
        self.__game = Game()
        self.__clock = Clock()

    def start(self):
        self.__game.start()
        self.__console_run = True

        try:
            while self.__console_run:
                Time.delta = self.__clock.tick(self.__max_fps)
                Time.cur_time += Time.delta

                self.__game.update()
        except KeyboardInterrupt:
            pass
        finally:
            self.__console_run = False
            self.__game.stop()
