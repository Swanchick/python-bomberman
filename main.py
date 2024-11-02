from networking import ServerNetwork, Network
from game.game import Game
from window import Window
from console import Console
from sys import argv
from settings import Settings


RES = Settings.res()


def main():    
    if "--console" in argv:
        console = Console()
        console.start()
        
        return

    window = Window(RES, "Bomber man", 60)
    window.start()


if __name__ == "__main__":
    main()
