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
