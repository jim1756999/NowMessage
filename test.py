from socket import socket
from typing import Mapping
import debug
import doctest

def main():
    doctest.testmod()
def test(i):
    '''
    >>> test(1)
    [DEBUG] Output is 1
    '''
    print("[DEBUG] Output is", i)
    tt = "tt"
    return tt
test(1)
main()

socket.accept()