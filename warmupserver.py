from udp import udpserver
import sys
import os

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
        clnt_sock.send("PONG")
        clnt_sock.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: {} host server_port".format(sys.argv[0])
        sys.exit()
    server_port = sys.argv[2]
    host = sys.argv[1]
    valid_port, err = validate_port(server_port)
    if valid_port is False:
        print err
        sys.exit()

    server = udpserver.UdpServer(host, int(server_port))
    main_loop(server)

