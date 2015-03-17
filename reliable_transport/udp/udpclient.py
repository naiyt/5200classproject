import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_packet(self, to_send):
        self.clnt_sock.sendto(to_send, (self.host, self.port))
