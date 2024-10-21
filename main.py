from networking import ServerNetwork, Network
from game.game import Game
from window import Window
from console import Console
from sys import argv
from settings import Settings


RES = Settings.res()


def main():    
    if "--server" in argv:
        server = ServerNetwork("127.0.0.1", 50000)
        server.init_server()
        server.start()

        Network.set(server)

        console = Console()
        console.start()
        return

    window = Window(RES, "Bomber man", 60)
    window.start()


if __name__ == "__main__":
    main()
