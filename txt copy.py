from multiprocessing import Process

from client import *
from config import *


def main():
    # use the get_name fuction to get the username
    name = input("User name: ")

    # create two sockets
    # the socket sock_client is a TCP client, responsible for the communication between the server and the client
    # the socket pipe_server is also a TCP client，but it acts as a conduit, responsible for receiving keyboard input
    sock_client = client(SOCK_ADDR)
    sock_client.send(bytes(name + Join_Room + "\n", "UTF-8"))
    pipe_server = server(CLI_PIPE_ADDR)

    # start a sub process, execute connect fuction
    p = Process(target=connect, args=(sock_client, pipe_server, name))
    p.daemon = True
    p.start()

    # receiving keyboard input cyclically

    while True:
        try:
            # from the standard input stream（keyboard）read a line
            data = sys.stdin.readline()
        except KeyboardInterrupt:
            # if an exit/abort signal is encountered, send an exit message, close the socket, terminate the sub process, and exit the program
            sock_client.send(bytes(name + Exit_Room + "\n", "UTF-8"))
            sock_client.close()
            pipe_server.close()
            p.terminate()
            break

        if not data:
            # if the data retrieved from the keyboard is empty, continue the loop
            continue
        else:
            # get the keyboard data，create a client socket pipe_client，and transfer the keyboard input to pipe_server
            pipe_client = client(CLI_PIPE_ADDR)
            pipe_client.send(bytes(data, "UTF-8"))
            pipe_client.close()


main()
