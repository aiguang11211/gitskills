#!usr/bin/env python
from socket import *
HOST='127.0.0.1'
PORT=1234
BUFSIZ=1024
ADDR=(HOST,PORT)
while True:
    tcpClient=socket(AF_INET,SOCK_STREAM)
    tcpClient.connect(ADDR)
    data=input('> ')
    if not data:
        break
    tcpClient.send(('%s\r\n'%data).encode())
    data=tcpClient.recv(BUFSIZ)
    if not data:
        break
    print(data.decode().strip())
    tcpClient.close()