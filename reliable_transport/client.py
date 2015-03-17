import socket
from udp import udpclient

class Client:
    def __init__(self, host, port, packet_size=500):
        self.host = host
        self.port = port
        self.packet_size = packet_size
        self.udp_connection = udpclient.Client(self.host, self.port)

    def transmit_file(self, filename):
        pass # Here, it should break up the packets and start sending them through
             # self.udp_connection.send_packet() per packet, using the appropriate reliability method

'''
Old transmission algo:


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
'''
