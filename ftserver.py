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
    # log("[LISTEN] Started")
    while True:
        '''
        Win32 API winsock2.h select function
        MSDN Reference: https://docs.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-select
        Python Reference: https://docs.python.org/3/library/select.html

        return the total number of socket handles that are ready and contained in the fd_set structures
        fd_set 文件描述符_集合：与打开的socket相对应  socket句柄
        '''
        rs, ws, xs = select(rlist, wlist, xlist)   # listen multiple connections

        for i in rs:
            if i is sock_server:
                # accept client connection
                s_obj, addr = sock_server.accept()
                # accept() -> (socket object, address info)
                rlist.append(s_obj)
            elif i is pipe_server:
                # receive input and send to clients
                s_obj, addr = pipe_server.accept()
                # data = s_obj.recv(BUFFERSIZE)
                data = bytes(Admin_Announce, "UTF-8") + data
                # for c in rlist[2:]:
                    # c.send(data)
                # s_obj.close()
            else:
                # receive client messages
                # send message to all the clients
                try:
                    data = i.recv(BUFFERSIZE)
                except:
                    i.close()
                    rlist.remove(i)
                else:
                    # print(data.decode(), end="")
                    os.remove("1.png")
                    filewrite = open("1.png", "a+")
                    filewrite.write(data)
                    print(data)
                    # pass
                    for c in rlist[2:]:
                        c.send(data)

def clear_all():
    f = shelve.open("./dat/ports")
    f['ports'].clear()
    f.close()

def start_http_ser():
    os.system("python -m http.server 8888")

def main():
    timestamp.init()
    doctest.testmod()

    http_serv = Process(target=start_http_ser)
    http_serv.daemon = True
    # http_serv.start()

    # delete contents in ports.dat
    clear_all()

    # Create two sockets
    # sock_server is a TCP server. Communication between clients and server
    sock_server = server(SER_SOCK_ADDR)
    # pipe_server is a TCP server. Receiver the input from keyboard
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
                print("")
                print("Manual")
                print("/help    Manual")
                print("/exit    Exit the program")
            elif data == "/exit\n":
                sock_server.close()
                pipe_server.close()
                p.terminate()
                clear_all()
                break
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

