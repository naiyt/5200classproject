import sys
import time
import socket
from udp import udp
from defaults import *
from header import Header
import math

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
    def __init__(self, host, port, packet_size=PACKET_SIZE):
        self.host = host
        self.port = port
        self.packet_size = packet_size
        self.udp_connection = udp.Udp(self.port+1)
        self.window_size = WINDOW_SIZE
        self.queue = []
        self.seqn = 0
        self.window_base = 0
        self.window_max = self.window_size -1

    def transmit_data(self, data):
        self._handshake()
        print 'Beginning to transmit data...'
        self.data = data
        self._selective_repeat()

    def transmit_file(self, filename):
        self._handshake()
        print 'Beginning to transmit file...'
        self._transmit_filename(filename)
        with open(filename, 'r') as f:
            self.f = f
            self._selective_repeat()

    def _selective_repeat(self):
        while True:
            self._send_packets()

    def _send_packets(self):
        for pos in range(self.window_base, self.window_max+1):
            if pos >= len(self.queue):
                data = self.data[:500]
                self.data = self.data[500:]
                if not data:
                    self._finish()
                header = Header(self.seqn, self.received_seqn, pos, self.window_size, Header.checksum(data), ftp=True)
                packet = Packet(header.formatted+data)
                self.seqn += len(data)
                self.queue.append(packet)
            packet = self.queue[pos]
            if packet.state not in [RECEIVED, SENT] or packet.timeout():
                packet.send(self.udp_connection, self.host, self.port)
            self._receive()
        self._advance_window()

    def _receive(self):
        try:
            data = self.udp_connection.recv(non_blocking=True)
            packet = data[0]
            header = Header.parse(packet[:Header.size()])
            pos = header.ftp_pos
            self.received_seqn = header.seqn
            self.queue[pos].state = RECEIVED if header.ack else FAILED
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

    def _advance_window(self):
        for pos in range(self.window_base, self.window_max+1):
            packet = self.queue[pos]
            if packet.state == RECEIVED:
                # self.queue[pos] = None
                self.window_base += 1
                self.window_max += 1
            else:
                return

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
