import socket
from udp import udp
from header import Header

GOBACKN = True

class Client:
    def __init__(self, host, port, packet_size=500):
        self.host = host
        self.port = port
        self.packet_size = packet_size
        self.udp_connection = udp.Udp(self.port+1)

    def transmit_file(self, filename):
        if GOBACKN is True:
            self.go_back_n(filename)
        else:
            self.selective_repeat(filename)

    def go_back_n(self, filename):
        with open(filename, 'r') as f:
            while True:
                data = f.read(500-Header.size())
                header = Header(1, 1, 1, 1, data)
                if len(header.formatted) != Header.size():
                    raise Exception('Header size is wrong: should be {}, was {}'.format(Header.size(), len(header.formatted)))
                if not data:
                    break
                self.udp_connection.send_packet(header.formatted + data, self.host, self.port)

    def selective_repeat(self, filename):
        pass
