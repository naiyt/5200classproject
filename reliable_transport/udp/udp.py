import socket

class Udp:
    def __init__(self, port, packet_size=500):
        self.packet_size = packet_size
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.local_host = socket.gethostname()
        self.port = port

        self.serv_sock.bind((self.local_host, self.port))
        self.clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def recv(self, non_blocking=False):
        if non_blocking:
            self.serv_sock.setblocking(0)
        return self.serv_sock.recvfrom(self.packet_size)

    def send_packet(self, to_send, host, port):
        self.clnt_sock.sendto(to_send, (host, port))
