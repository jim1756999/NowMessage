# settings.py

import os
import shelve
from random import randint
from socket import *

# Supported language zh_cn, en_us
LANGUAGE = "en_uk"

HOST = "127.0.0.1"


# sever and client connection
SOCK_PORT = 47736
SOCK_ADDR = HOST, SOCK_PORT
BINDING = "0.0.0.0"
SER_SOCK_ADDR = BINDING, SOCK_PORT

# Socket address used by pipe_server and pipe_client in server server.py file
SER_PIPE_PORT = 48760
SER_PIPE_ADDR = HOST, SER_PIPE_PORT

# 客户端client.py文件中供pipe_server和pipe_client使用的套接字地址
# 因为每个客户端都必须有不同的套接字来作起到连接键盘输入和网络套接字之间的管道的作用
# 使用一个文件记录下每一次运行出现的端口号，以保证不重复
if not os.path.exists("./dat/ports.dat"):
    f = shelve.open("./dat/ports")
    f["ports"] = []
f = shelve.open("./dat/ports")
while True:
    n = randint(4500, 10000)
    if n not in f["ports"]:
        f['ports'].append(n)
        break
f.close()
CLI_PIPE_PORT = n
CLI_PIPE_ADDR = HOST, CLI_PIPE_PORT

# 缓冲区大小
BUFFERSIZE = 100

# 返回一个TCP服务端套接字


def server(addr):
    sock = socket(AF_INET, SOCK_STREAM, 0)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(10)
    return sock

# 返回一个TCP客户端套接字


def client(addr):
    sock = socket(AF_INET, SOCK_STREAM, 0)
    sock.connect(addr)
    return sock
