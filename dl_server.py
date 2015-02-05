from udp import udpserver
import sys
import os
import time
import datetime

OUTPUTFILE = 'output.dat'

def validate_port(port):
    if port.isdigit():
        port = int(port)
        if port > 0 and port <= 61000:
            return True, "Valid"
        else:
            return False, "Port must be between 0 and 61000"
    else:
        return False, "Port must be a digit"

def main_loop(server):
    while True:
        clnt_sock, addr = server.serv_sock.accept()
        filename = clnt_sock.recv(500)
        print "Receiving data for: {}".format(filename)
        f = open(OUTPUTFILE, 'w')
        start_time = datetime.datetime.now()
        size = 0
        clnt_sock.send("")
        while True:
            data = clnt_sock.recv(500)
            f.write(data)
            if len(data) == 0:
                break
        end_time = datetime.datetime.now()
        time_elapsed = end_time - start_time
        file_size = os.path.getsize(OUTPUTFILE)
        throughput = (file_size / 125) / time_elapsed.total_seconds()
        print "Throughput: {} kbps".format(round(throughput, 2))
        f.close()
        clnt_sock.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: {} host server_port".format(sys.argv[0])
        sys.exit()
    server_port = sys.argv[1]
    valid_port, err = validate_port(server_port)
    if valid_port is False:
        print err
        sys.exit()

    server = udpserver.UdpServer(int(server_port))
    main_loop(server)

