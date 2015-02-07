import socket

class UdpServer:
    def __init__(self, port, tcp=False, num_connections=5):
        if tcp:
          self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
          self.serv_sock = socket.socket()
        self.host = socket.gethostname()
        self.port = port
        self.serv_sock.bind((self.host, self.port))
        self.serv_sock.listen(num_connections)
