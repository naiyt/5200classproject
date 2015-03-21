import datetime
from udp import udp
from header import Header

STARTING_SEQN = 0
WINDOW_SIZE = 5

class Server:
    def __init__(self, port):
        self.port = port
        self.udp_server = udp.Udp(self.port)

    def main_loop(self):
        while True:
            start_time = datetime.datetime.now()
            self.receive_loop()
            self._calc_throughput(start_time, datetime.datetime.now(), os.path.getsize(filename))

    def ack(self, received_header, host):
        header = Header(self.seqn, received_header.ackn+1, WINDOW_SIZE, '', ack=True)
        self.udp_server.send_packet(header.formatted, host, self.port+1)

    def receive_loop(self):
        while True:
            data = self.udp_server.recv()
            packet = data[0]
            host = data[1][0]
            header = Header.parse(packet[:Header.size()])
            data = packet[Header.size():]
            if header.syn:
                self._handshake(header, host)
            else:
                if header.file_name:
                    self.f = open(data+'out', 'w')
                    print 'Opening file {}out'.format(data)
                elif header.seqn == self.seqn and self._validate_checksum(header.checksum, data):
                    self.f.write(data)
                    self.seqn += 1
                elif header.fin:
                    self.f.close()
                    print 'finished transmitting file'
                # else:
                    # print "got {}, wanted {}".format(header.seqn, self.seqn)
                    # print 'bad packet, going back n'
                self.ack(header, host)

    def _handshake(self, header, host):
        print 'Initiating client handshake...'
        self.seqn = header.seqn
        self._send_syn_ack(header, host)
        self._wait_for_ack()

    def _send_syn_ack(self, header, host):
        print 'Sending syn-ack...'
        header = Header(self.seqn, header.seqn+1, header.window_size, '', syn=True, ack=True)
        self.udp_server.send_packet(header.formatted, host, self.port+1)

    def _wait_for_ack(self):
        print 'Waiting for client ack...'
        ack = self.udp_server.recv()
        print 'Client ack received'

    def _calc_throughput(self, start_time, end_time, file_size):
        time_elapsed = end_time - start_time
        file_size = os.path.getsize(OUTPUTFILE)
        throughput = (file_size / 125) / time_elapsed.total_seconds()
        print "Throughput: {} kbps".format(round(throughput, 2))

    def _validate_checksum(self, checksum, data):
        if Header.checksum(data) != checksum:
            return False
        else:
            return True
