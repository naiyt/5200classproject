from udp import udpserver
from header import Header

class Server:
    def __init__(self, port):
        self.port = port
        self.udp_server = udpserver.Server(self.port)

    def main_loop(self):
        while True:
            filename = self.udp_server.recv()
            print 'Receiving data for : {}'.format(filename)
            f = open(filename)
            start_time = datetime.datetime.now()

            self.ack()
            self.receive_loop(f)
            self.calc_throughput(start_time, datetime.datetime.now(), os.path.getsize(filename))

            f.close()

    def ack(self):
        print "ACKING - TODO: add ack code"

    def receive_loop(self, out_file):
        while True:
            data = self.udp_server.recv()
            print data
            self.ack()
            out_file.write(data)
            if len(data) == 0:
                return

    def calc_throughput(self, start_time, end_time, file_size):
        time_elapsed = end_time - start_time
        file_size = os.path.getsize(OUTPUTFILE)
        throughput = (file_size / 125) / time_elapsed.total_seconds()
        print "Throughput: {} kbps".format(round(throughput, 2))
