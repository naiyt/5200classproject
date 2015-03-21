import socket
from udp import udp
from header import Header
from threading import Thread
import sys
import time

STARTING_SEQN = 0
WINDOW_SIZE = 5
QUEUE_SIZE = 50
INIT = 'init'
SENT = 'sent'
RECEIVED = 'received'
TIMEOUT = 1.0

class Packet:
    def __init__(self, packet):
        self.packet = packet
        self.state = INIT

    def send(self, connection, host, port):
        connection.send_packet(self.packet, host, port)
        self.state = SENT
        self.timestamp = time.time()

    def timeout(self):
        if time.time() - self.timestamp > TIMEOUT:
            return True
        else:
            return False


class Client:
    def __init__(self, host, port, packet_size=500):
        self.host = host
        self.port = port
        self.packet_size = packet_size
        self.udp_connection = udp.Udp(self.port+1)
        self.window_size = WINDOW_SIZE

    def transmit_file(self, filename):
        self._handshake()
        print 'Beginning to transmit file...'
        self._transmit_filename(filename)
        self.go_back_n(filename)

    def go_back_n(self, filename):
        self.queue = []
        self.seqn = 0
        self.seq_base = 0
        self.seq_max = self.window_size -1

        with open(filename, 'r') as f:
            while True:
                if self.seqn < self.seq_max:
                    if self.seqn == len(self.queue):
                        data = f.read(500-Header.size())
                        if not data:
                            header = Header(self.seqn, 1, self.window_size, '', fin=True)
                            Packet(header.formatted).send(self.udp_connection, self.host, self.port)
                            print 'Finished transfer!'
                            sys.exit()
                        header = Header(self.seqn, 1, self.window_size, Header.checksum(data))
                        packet = Packet(header.formatted + data)
                        self.queue.append(packet)
                    else:
                        packet = self.queue[self.seqn]
                        packet.state = INIT
                    packet.send(self.udp_connection, self.host, self.port)
                    self.receive()
                    self.seqn += 1
                elif self.queue[self.seq_base].timeout():
                    for packet in self.queue[self.seq_base:self.seq_max]:
                        packet.state = INIT
                    self.seqn = self.seq_base

    def receive(self):
        try:
            data = self.udp_connection.recv(non_blocking=True)
            packet = data[0]
            header = Header.parse(packet[:Header.size()])
            if header.ack:
                self.queue[self.seqn].state = RECEIVED
                self.seq_max += (header.seqn-self.seq_base)
                self.seq_base = header.seqn
                self.seqn = header.seqn
            else:
                print 'did not ack'
        except socket.error:
            pass


    def _transmit_filename(self, filename):
        header = Header(0,0, 5, Header.checksum(filename), file_name=True)
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
        header = Header(STARTING_SEQN, 0, 5, '', syn=True)
        self.udp_connection.send_packet(header.formatted, self.host, self.port)

    def _wait_for_syn_ack(self):
        syn_ack = self.udp_connection.recv()[0]
        header = Header.parse(syn_ack[:Header.size()])
        if header.syn is False or header.ack is False:
            raise Exception('The server did not respond with a SYN-ACK')
        return header.seqn

    def _send_ack(self, received_seqn):
        header = Header(STARTING_SEQN+1, received_seqn+1, 5, '', ack=True)
        self.udp_connection.send_packet(header.formatted, self.host, self.port)
