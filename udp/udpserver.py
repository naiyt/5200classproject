import socket

class UdpServer:
    def __init__(self, port, tcp=False, num_connections=5):
        protocol = socket.SOCK_STREAM if tcp else socket.SOCK_DGRAM
        self.serv_sock = socket.socket(socket.AF_INET, protocl)
        self.host = socket.gethostname()
        self.port = port
        self.serv_sock.bind((self.host, self.port))
        self.serv_sock.listen(num_connections)
