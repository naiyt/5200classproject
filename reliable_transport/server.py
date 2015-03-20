import datetime
from udp import udp
from header import Header

STARTING_SEQN = 0

class Server:
    def __init__(self, port):
        self.port = port
        self.udp_server = udp.Udp(self.port)

    def main_loop(self):
        while True:
            start_time = datetime.datetime.now()
            self.receive_loop()
            self._calc_throughput(start_time, datetime.datetime.now(), os.path.getsize(filename))

    def ack(self):
        print "ACKING - TODO: add ack code"

    def receive_loop(self):
        while True:
            data = self.udp_server.recv()
            packet = data[0]
            host_and_port = data[1]
            header = Header.parse(packet[:Header.size()])
            data = packet[Header.size():]
            if header.syn:
                self._handshake(header, host_and_port)

    def _handshake(self, header, host_and_port):
        print 'Initiating client handshake...'
        self._send_syn_ack(header, host_and_port)
        self._wait_for_ack()

    def _send_syn_ack(self, header, host_and_port):
        print 'Sending syn-ack...'
        header = Header(STARTING_SEQN, header.seqn+1, header.window_size, '', syn=True, ack=True)
        self.udp_server.send_packet(header.formatted, host_and_port[0], self.port+1)

    def _wait_for_ack(self):
        print 'Waiting for client ack...'
        ack = self.udp_server.recv()

    def _calc_throughput(self, start_time, end_time, file_size):
        time_elapsed = end_time - start_time
        file_size = os.path.getsize(OUTPUTFILE)
        throughput = (file_size / 125) / time_elapsed.total_seconds()
        print "Throughput: {} kbps".format(round(throughput, 2))
