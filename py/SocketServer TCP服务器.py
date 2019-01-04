#!usr/bin/env python
from socketserver import TCPServer as tcp,StreamRequestHandler as SRH
from time import ctime

HOST='0.0.0.0'
PORT=1234
ADDR=(HOST,PORT)

class MyRequestHandler(SRH):
    def handle(self):
        print('...connected from:',self.client_address)
        self.wfile.write(('[%s]%s'%(ctime(),self.rfile.readline().decode())).encode())

tcpserver=tcp(ADDR,MyRequestHandler)
print('waiting for connection...')
tcpserver.serve_forever()

