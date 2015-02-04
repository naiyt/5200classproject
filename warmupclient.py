from udp import udpclient
import re
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

ifip = re.compile('\s*((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|localhost)\s*')

def validate_ip(ip):
    if ifip.match(ip):
        return True, "Valid"
    return False, "Not a valid ipv4 IPaddress or localhost"

def validate_file(filename):
    return os.path.exists(filename)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {} hostname port filename".format(sys.argv[0])
    else:
        host = sys.argv[1]
        port = sys.argv[2]
        filename = sys.argv[3]
        valid_port, err = validate_port(port)
        if valid_port is False:
            print err
            sys.exit()
        if validate_file(filename) is False:
            print "{} does not exist".format(filename)
            sys.exit()
        
        # host validation
        valid_host, err_host = validate_ip(host)
        if valid_host is False:
            print err_host
            sys.exit()
        
        client = udpclient.UdpClient(host, int(port))
        client.connect()
        client.transmit(filename)
        
        # send file
        



"""
regex for valid IPaddresses 
\s*((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|localhost)\s*
"""
