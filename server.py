# server.py

import doctest
import shelve
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
    exlist = [] # exceptional

    print(Wait_Conn)    # print info
    while True:
        rs, ws, xs = select(rlist, wlist, exlist)   # listen multiple connections

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
                # 接收客户端信息
                # 将客户端信息发送到所有的客户端中去
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

def main():
    doctest.testmod()

    # delete contents in ports.dat
    clear_all()

    # Create two sockets
    # sock_server is a TCP server. Communication between clients and server
    sock_server = server(SOCK_ADDR)
    # pipe_server is a TCP server. Receiver the input from keyborad
    pipe_server = server(SER_PIPE_ADDR)
    

    # 开始一个子进程，执行listen函数
    p = Process(target=listen, args=(sock_server, pipe_server))
    p.daemon = True
    p.start()
    
    # 循环接收键盘输入
    while True:
        try:
            # 从标准输入流（键盘）读取一行
            data = sys.stdin.readline()
        except KeyboardInterrupt:
            # 如果遇到退出/中止信号，关闭套接字，结束子进程，退出程序
            sock_server.close()
            pipe_server.close()
            p.terminate()
            clear_all()
            break

        if not data:
            # 如果从键盘获取数据为空，继续循环
            continue
        else:
            # 获得键盘数据，创建客户端套接字pipe_client，将键盘输入传输给pipe_server
            pipe_client = client(SER_PIPE_ADDR)
            pipe_client.send(bytes(data, "UTF-8"))
            pipe_client.close()

if __name__ == '__main__':
    main()
