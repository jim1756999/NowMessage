# server.py

import doctest
import sys
from multiprocessing import Process
from select import select
from socket import *

from config import *
from debug import *
from i18n import *


def listen(sock_server, pipe_server):
    # IO multiplexing: loop listening socket
    rlist = [sock_server, pipe_server]  # readable
    wlist = []
    xlist = [] # exceptional

    print(Wait_Conn)    # print info
    while True:
        rs, ws, xs = select(rlist, wlist, xlist)   # listen multiple connections

        for r in rs:
            if r is sock_server:
                # accept client connection
                conn, addr = sock_server.accept()
                rlist.append(conn)
            elif r is pipe_server:
                # receive input and send to clients
                conn, addr = pipe_server.accept()
                data = conn.recv(BUFFERSIZE)
                data = bytes(Admin_Announce, "UTF-8") + data
                for c in rlist[2:]:
                    c.send(data)
                conn.close()
            else:
                # receive client messages
                # send message to all the clients
                try:
                    data = r.recv(BUFFERSIZE)
                except:
                    r.close()
                    rlist.remove(r)
                else:
                    print(data.decode(), end="")
                    for c in rlist[2:]:
                        c.send(data)

def clear_all():
    f = shelve.open("ports")
    f['ports'].clear()
    f.close()

def start_http_ser():
    os.system("python -m http.server 8888")

def main():
    timestamp.init()
    doctest.testmod()

    http_serv = Process(target=start_http_ser)
    http_serv.daemon = True
    http_serv.start()

    # delete contents in ports.dat
    clear_all()

    # Create two sockets
    # sock_server is a TCP server. Communication between clients and server
    sock_server = server(SER_SOCK_ADDR)
    # pipe_server is a TCP server. Receiver the input from keyborad
    pipe_server = server(SER_PIPE_ADDR)
    

    # create a subprocess, excuting listen()
    p = Process(target=listen, args=(sock_server, pipe_server))
    p.daemon = True
    p.start()
    
    # loop receive input from keyboard
    while True:
        try:
            # read a line from standard input stream
            data = sys.stdin.readline()
            if data == "/help\n":
                print("man page")
        except KeyboardInterrupt:
            # If an exit/abort signal is encountered, close the socket, end the child process, and exit the program
            sock_server.close()
            pipe_server.close()
            p.terminate()
            clear_all()
            break

        if not data:
            # If the data obtained from the keyboard is empty, continue to loop
            continue
        else:
            # Obtain keyboard data, create a client client pipe_client, and transmit keyboard input to pipe_server
            pipe_client = client(SER_PIPE_ADDR)
            pipe_client.send(bytes(data, "UTF-8"))
            pipe_client.close()

if __name__ == '__main__':
    main()
