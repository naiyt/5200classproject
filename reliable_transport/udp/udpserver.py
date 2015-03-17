import socket

class Server:
    def __init__(self, port, packet_size=500):
        self.packet_size = packet_size
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = socket.gethostname()
        self.port = port
        self.serv_sock.bind((self.host, self.port))

    def recv(self):
        data = self.serv_sock.recvfrom(self.packet_size) # It returns a tuple, where the first entry is the data, second is the ip received from
        return data[0]
