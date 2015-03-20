import socket
from udp import udp
from header import Header

GOBACKN = True
STARTING_SEQN = 0

class Client:
    def __init__(self, host, port, packet_size=500):
        self.host = host
        self.port = port
        self.packet_size = packet_size
        self.udp_connection = udp.Udp(self.port+1)

    def transmit_file(self, filename):
        self._handshake(filename)
        if GOBACKN is True:
            self.go_back_n(filename)
        else:
            self.selective_repeat(filename)

    def go_back_n(self, filename):
        with open(filename, 'r') as f:
            while True:
                data = f.read(500-Header.size())
                header = Header(1, 1, 1, data)
                if len(header.formatted) != Header.size():
                    raise Exception('Header size is wrong: should be {}, was {}'.format(Header.size(), len(header.formatted)))
                if not data:
                    break
                self.udp_connection.send_packet(header.formatted + data, self.host, self.port)

    def selective_repeat(self, filename):
        pass

    def _handshake(self):
        print 'Starting handshake...'
        self._send_syn()
        received_seqn = self._wait_for_syn_ack()
        self._send_ack(received_seqn)

    def _send_syn(self):
        print 'Sending syn...'
        header = Header(STARTING_SEQN, 0, 5, '', syn=True)
        self.udp_connection.send_packet(header.formatted, self.host, self.port)

    def _wait_for_syn_ack(self):
        print 'Waiting for syn-ack from server...'
        syn_ack = self.udp_connection.recv()[0]
        header = Header.parse(syn_ack[:Header.size()])
        if header.ackn != STARTING_SEQN+1:
            raise Exception('Incorrect received seqn: should be {}, was {}'.format(STARTING_SEQN+1, header.ackn))
        if header.syn is False or header.ack is False:
            raise Exception('The server did not respond with a SYN-ACK')
        print 'syn-ack received...'
        return header.seqn

    def _send_ack(self, received_seqn):
        print 'Sending final ack to server...'
        header = Header(STARTING_SEQN+1, received_seqn+1, 5, '', ack=True)
        self.udp_connection.send_packet(header.formatted, self.host, self.port)
