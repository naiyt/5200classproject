import os
import datetime
from udp import udp
from defaults import *
from header import Header

class Server:
    def __init__(self, port):
        self.port = port
        self.udp_server = udp.Udp(self.port)
        self.ftp_pos = 0

    def ack(self, received_header, host):
        header = Header(self.seqn, received_header.seqn+self.data_len, received_header.ftp_pos, WINDOW_SIZE, '')
        self.udp_server.send_packet(header.formatted, host, self.port+1)

    def receive_loop(self):
        while True:
            data = self.udp_server.recv()
            packet = data[0]
            host = data[1][0]
            header = Header.parse(packet[:Header.size()])
            data = packet[Header.size():]
            self.data_len = len(data)
            if header.syn:
                self._handshake(header, host)
            else:
                self._check_packet(data, header, host)

    def _check_packet(self, data, header, host):
        # print 'header: {}, self: {}'.format(header.ftp_pos, self.ftp_pos)
        if header.file_name:
            self.file_name = data
            if LOCAL:
                self.f = open(self.file_name+'out', 'w')
            else:
                self.f = open(self.file_name, 'w')
            self.start_time = datetime.datetime.now()
            print 'Opening file {}out'.format(data)
        elif header.ftp_pos == self.ftp_pos and self._validate_checksum(header.checksum, data):
            self.f.write(data)
            self.ftp_pos += 1
        elif header.fin:
            print 'finished transmitting file'
            self._calc_throughput(self.start_time, datetime.datetime.now(), self.file_name)
            self.f.close()
        else:
            pass # Either invalid checksum or seqn out of ourder
        self.ack(header, host)

    def _validate_checksum(self, checksum, data):
        return Header.checksum(data) == checksum

    #########################3
    #  Handshake
    #########################3

    def _handshake(self, header, host):
        print 'Initiating client handshake...'
        self.seqn = header.seqn
        self._send_syn_ack(header, host)
        self._wait_for_ack()

    def _send_syn_ack(self, header, host):
        header = Header(self.seqn, header.seqn+1, 0, header.window_size, '', syn=True, ack=True)
        self.udp_server.send_packet(header.formatted, host, self.port+1)

    def _wait_for_ack(self):
        ack = self.udp_server.recv()

    def _calc_throughput(self, start_time, end_time, file_name):
        time_elapsed = end_time - start_time
        file_size = os.path.getsize(file_name)
        throughput = (file_size / 125) / time_elapsed.total_seconds()
        print "Throughput: {} kbps".format(round(throughput, 2))
