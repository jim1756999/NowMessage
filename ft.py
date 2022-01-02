# client.py
import math
import os
import pickle
import sys
from multiprocessing import Process
from select import select
from socket import *

import config
from config import *
from i18n import *



current_chunk = 1


def connect(sock_client, pipe_server):
    # IO multiplexing：loop listening socket
    rlist = [sock_client, pipe_server]
    wlist = []
    xlist = []

    while True:
        rs, ws, xs = select(rlist, wlist, xlist)

        for r in rs:
            if r is sock_client:
                # accept server information
                # data = sock_client.recv(BUFFERSIZE).decode()
                # print(data, end="")
                pass
            elif r is pipe_server:
                # accept keyboard input and send to server
                conn, addr = pipe_server.accept()
                data = conn.recv(BUFFERSIZE)
                sock_client.send(data)
                conn.close()


# def get_FileSize(filePath):

#     fsize = os.path.getsize(filePath)
#     fsize = fsize/float(1024 * 1024)

#     return round(fsize, 2)


def link():
    # create two sockets
    # the socket sock_client is a TCP client, responsible for the communication between the server and the client
    # the socket pipe_server is also a TCP client，but it acts as a conduit, responsible for receiving keyboard input
    global sock_client
    global pipe_server
    sock_client = client(SOCK_ADDR)
    pipe_server = server(CLI_PIPE_ADDR)

    # start a sub process, execute connect fuction
    global pcon
    pcon = Process(target=connect, args=(sock_client, pipe_server))
    pcon.daemon = True
    pcon.start()


def readfile():
    # receiving keyboard input cyclically
    while True:
        try:
            # from the standard input stream（keyboard）read a line
            filename = sys.stdin.readline()
            data = chunk_file(filename)

            # openfile = open(filename, mode="rb")
            # data = openfile.read()
        except KeyboardInterrupt:
            # if an exit/abort signal is encountered, send an exit message, close the socket, terminate the sub process, and exit the program
            sock_client.close()
            pipe_server.close()
            pcon.terminate()
            break

        if not data:
            # if the data retrieved from the keyboard is empty, continue the loop
            continue
        else:
            # get the keyboard data，create a client socket pipe_client，and transfer the keyboard input to pipe_server
            pipe_client = client(CLI_PIPE_ADDR)
            # dataencoded = pickle.dumps(data)
            pipe_client.send(bytes(data))
            pipe_client.close()


def chunk_file(filename):
    filename = filename[:-1]
            # print(filename)
            # BUFFERSIZE = filesize
    chunk_size = 100*1024
    total_size = os.path.getsize(filename)
    current_chunk = 1
    total_chunk = math.ceil(total_size / chunk_size)
    # while current_chunk <= total_chunk:
    #     start = (current_chunk - 1) * chunk_size
    #     end = min(total_size, start + chunk_size)
    #     with open(filename, 'rb') as f:
    #         f.seek(start)
    #         file_chunk_data = f.read(end-start)
    #         data = file_chunk_data
    return data


def main():
    link()
    readfile()


if __name__ == '__main__':
    main()
