import socket
from udp import udpclient
from header import Header

GOBACKN = True

class Client:
    def __init__(self, host, port, packet_size=500):
        self.host = host
        self.port = port
        self.packet_size = packet_size
        self.udp_connection = udpclient.Client(self.host, self.port)

    def transmit_file(self, filename):
        if GOBACKN is True:
            self.go_back_n(filename)
        else:
            self.selective_repeat(filename)

    def go_back_n(self, filename):
        with open(filename, 'r') as f:
            while True:
                header = Header(1, 1, 1, 1)
                if len(header.formatted) != Header.size():
                    raise 'Header size is wrong'
                byte_s = f.read(500-Header.size())
                if not byte_s:
                    break
                self.udp_connection.send_packet(header.formatted + byte_s)

    def selective_repeat(self, filename):
        pass
