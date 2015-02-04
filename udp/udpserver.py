import socket

class UdpServer:
    def __init__(self, port, num_connections=5):
        self.serv_sock = socket.socket()
        self.host = socket.gethostname()
        self.port = port
        self.serv_sock.bind((self.host, self.port))
        self.serv_sock.listen(num_connections)
                




"""
import socket

## 1. construct a server socket object
serv_sock = socket.socket()

## 2. get the hostname
host = socket.gethostname()
print 'host:', host
## 3. set the port number
port = 1234
print 'port:', port

## 4. bind the socket to the host
##    and the port
serv_sock.bind((host, port))

## 5. specify the number of connections
##    that can be queued up on the
##    socket.
serv_sock.listen(5)

## 6. go into infinite loop
while True:
    ## 6.1. accept connections
    clnt_sock, addr = serv_sock.accept()
    ## 6.2. print the address of the connection
    print 'Got connection from', addr
    ## 6.3. send a simple string
    clnt_sock.send('Thank you for connecting')
    ## 6.4 close the connection
    clnt_sock.close()
"""