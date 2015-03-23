import sys
import time
import socket
from udp import udp
from defaults import *
from header import Header

class Packet:
    def __init__(self, packet):
        self.packet = packet
        self.state = INIT

    def send(self, connection, host, port):
        connection.send_packet(self.packet, host, port)
        self.state = SENT
        self.timestamp = time.time()

    def timeout(self):
        return time.time() - self.timestamp > TIMEOUT

class Client:
    def __init__(self, host, port, packet_size=500):
        self.host = host
        self.port = port
        self.packet_size = packet_size
        self.udp_connection = udp.Udp(self.port+1)
        self.window_size = WINDOW_SIZE
        self.queue = []
        self.seqn = 0
        self.window_base = 0
        self.window_max = self.window_size -1
        self.ftp_pos = 0
        self.win_pos = 0

    def transmit_file(self, filename):
        self._handshake()
        print 'Beginning to transmit file...'
        self._transmit_filename(filename)
        with open(filename, 'r') as f:
            self.f = f
            self._go_back_n(filename)

    def _go_back_n(self, filename):
        while True:
            if self.win_pos in range(self.window_base, self.window_max+1):
                print self.win_pos
                self._send_packets()
            elif self.queue[self.window_base].timeout():
                for packet in self.queue[self.window_base:self.window_max]:
                    packet.state = INIT
                self.win_pos = self.window_base

    def _send_packets(self):
        up_seq = False
        if self.win_pos == len(self.queue):
            data = self.f.read(PACKET_SIZE)
            if not data:
                self._finish()
            header = Header(self.seqn, self.received_seqn, self.win_pos, self.window_size, Header.checksum(data), ftp=True)
            packet = Packet(header.formatted + data)
            self.queue.append(packet)
            up_seq = True
        else:
            packet = self.queue[self.win_pos]
            packet.state = INIT
        packet.send(self.udp_connection, self.host, self.port)
        self._receive()
        if up_seq:
            self.win_pos += 1

    def _receive(self):
        try:
            data = self.udp_connection.recv(non_blocking=True)
            packet = data[0]
            header = Header.parse(packet[:Header.size()])
            self.window_max += (header.ftp_pos-self.window_base)
            self.window_base = header.ftp_pos
            self.ftp_pos = header.ftp_pos
            self.win_pos = self.ftp_pos
            if header.ack:
                self.queue[self.ftp_pos-1].state = RECEIVED
        except socket.error:
            pass

    def _finish(self):
        header = Header(self.seqn, 1, 0, self.window_size, '', fin=True)
        Packet(header.formatted).send(self.udp_connection, self.host, self.port)
        print 'Finished transfer!'
        sys.exit()

    def _transmit_filename(self, filename):
        header = Header(self.seqn, self.received_seqn, 0, self.window_size, Header.checksum(filename), file_name=True)
        self.udp_connection.send_packet(header.formatted+filename, self.host, self.port)
        ack = self.udp_connection.recv()

    #########################3
    #  Handshake
    #########################3
    def _handshake(self):
        print 'Starting handshake...'
        self._send_syn()
        received_seqn = self._wait_for_syn_ack()
        self._send_ack(received_seqn)

    def _send_syn(self):
        header = Header(STARTING_SEQN, 0, 0, self.window_size, '', syn=True)
        self.udp_connection.send_packet(header.formatted, self.host, self.port)

    def _wait_for_syn_ack(self):
        syn_ack = self.udp_connection.recv()[0]
        header = Header.parse(syn_ack[:Header.size()])
        self.received_seqn = header.seqn
        if header.syn is False or header.ack is False:
            raise Exception('The server did not respond with a SYN-ACK')
        return header.seqn

    def _send_ack(self, received_seqn):
        self.seqn += 1
        header = Header(self.seqn, received_seqn+1, 0, self.window_size, '', ack=True)
        self.udp_connection.send_packet(header.formatted, self.host, self.port)
