import socket

class UdpServer:
    def __init__(self, port, num_connections=5):
        self.serv_sock = socket.socket()
        self.host = socket.gethostname()
        self.port = port
        self.serv_sock.bind((self.host, self.port))
        self.serv_sock.listen(num_connections)
