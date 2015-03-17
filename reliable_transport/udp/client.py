import socket

class Client:
    def __init__(self, host, port, packet_size=500):
        self.packet_size = packet_size
        self.host = host
        self.port = port
        self.clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_packet(self, to_send):
        self.clnt_sock.sendto(to_send, (self.host, self.port))

    # def transmitFile(self, filename):
    #     self.send(filename)
    #
    #     if self.tcp:
    #         self.clnt_sock.recv(500)
    #
    #     with open(filename, 'r') as f:
    #         while True:
    #             byte_s = f.read(500)
    #             if not byte_s:
    #                 break
    #             self.send(byte_s)
    #     self.send("")

    # def send(self, to_send):
    #     if self.tcp:
    #         self.clnt_sock.send(to_send)
    #     else:
    #         self.clnt_sock.sendto(to_send, (self.host, self.port))
