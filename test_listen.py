from server import *
from config import *

# Create two sockets
# sock_server is a TCP server. Communication between clients and server
sock_server = server(SER_SOCK_ADDR)
# pipe_server is a TCP server. Receiver the input from keyborad
pipe_server = server(SER_PIPE_ADDR)

listen(sock_server, pipe_server)
