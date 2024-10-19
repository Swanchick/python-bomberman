from networking import ServerNetwork
from networking import ClientNetwork
from window import Window
from sys import argv

RES = (800, 600)

def main():
    if "--server" in argv:
        server = ServerNetwork("127.0.0.1", 50000)
        server.init_server()
        server.start()

        return

    if "--multiplayer" in argv:
        client = ClientNetwork("127.0.0.1", 50000)
        client.init_client()
        client.start()
    

    window = Window(RES, "Bomber man", 144)
    window.start()


if __name__ == "__main__":
    main()
