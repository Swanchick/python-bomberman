from networking import ServerNetwork, NETWORK
from window import Window
from sys import argv
from settings import Settings


RES = Settings.res()


def main():
    global NETWORK
    
    if "--server" in argv:
        server = ServerNetwork("127.0.0.1", 50000)
        server.init_server()
        server.start()

        NETWORK = server

        return

    window = Window(RES, "Bomber man", 144)
    window.start()


if __name__ == "__main__":
    main()
