from udp import server
import sys
import os
import time
import datetime

OUTPUTFILE = 'output.dat'
TCP = True

def validate_port(port):
    if port.isdigit():
        port = int(port)
        if port > 0 and port <= 61000:
            return True, "Valid"
        else:
            return False, "Port must be between 0 and 61000"
    else:
        return False, "Port must be a digit"

def receive_loop(server, outFile):
    while True:
        data = server.recv()
        outFile.write(data)
        if len(data) == 0:
            return

def calc_throughput(start_time, end_time, file_size):
    time_elapsed = end_time - start_time
    file_size = os.path.getsize(OUTPUTFILE)
    throughput = (file_size / 125) / time_elapsed.total_seconds()
    print "Throughput: {} kbps".format(round(throughput, 2))

def main_loop(server):
    while True:
        server.begin()
        filename = server.recv()

        print "Receiving data for: {}".format(filename)
        f = open(OUTPUTFILE, 'w')
        start_time = datetime.datetime.now()

        server.ack()
        receive_loop(server, f)
        calc_throughput(start_time, datetime.datetime.now(), os.path.getsize(OUTPUTFILE))

        f.close()
        server.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: {} host server_port".format(sys.argv[0])
        sys.exit()
    server_port = sys.argv[1]
    valid_port, err = validate_port(server_port)
    if valid_port is False:
        print err
        sys.exit()

    server = server.Server(int(server_port), TCP)
    main_loop(server)
