from server_network import ServerNetwork
from client_network import ClientNetwork
from sys import argv


def main():
    print(argv)

    if "--server" in argv:
        server = ServerNetwork("127.0.0.1", 50000)
        server.init_server()
        server.start()

        return


    client = ClientNetwork("127.0.0.1", 50000)
    client.init_client()
    client.start()


if __name__ == "__main__":
    main()
