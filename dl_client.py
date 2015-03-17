from reliable_transport import client
import re
import sys
import os
import socket

def validate_port(port):
    if port.isdigit():
        port = int(port)
        if port > 0 and port <= 61000:
            return True, "Valid"
        else:
            return False, "Port must be between 0 and 61000"
    else:
        return False, "Port must be a digit"

IPREGEX = re.compile('\s*((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|localhost)\s*')
def validate_ip(ip):
    if IPREGEX.match(ip):
        return True, "Valid"
    else:
        try:
            socket.gethostbyname(ip)
            print "It's a valid hostname"
            return True, "Valid"
        except socket.error:
            return False, "Not a valid ipv4 IPaddress or localhost"

def validate_file(filename):
    return os.path.exists(filename), "{} does not exist".format(filename)

def run_validations(host, port, filename):
    valid_port, err = validate_port(port)
    if valid_port is False:
        print err
        sys.exit()

    valid_file, err = validate_file(filename)
    if valid_file is False:
        print err
        sys.exit()

    valid_host, err = validate_ip(host)
    if valid_host is False:
        print err
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {} hostname port filename".format(sys.argv[0])
    else:
        host = sys.argv[1]
        port = sys.argv[2]
        filename = sys.argv[3]
        run_validations(host, port, filename)

        client = client.Client(host, int(port))
        client.transmit_file(filename)
        # client.connect()
        # client.transmitFile(filename)
