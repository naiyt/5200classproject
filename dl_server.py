from reliable_transport import server
import sys
import os
import time
import datetime

def validate_port(port):
    if port.isdigit():
        port = int(port)
        if port > 0 and port <= 61000:
            return True, "Valid"
        else:
            return False, "Port must be between 0 and 61000"
    else:
        return False, "Port must be a digit"

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: {} host server_port".format(sys.argv[0])
        sys.exit()
    server_port = sys.argv[1]
    valid_port, err = validate_port(server_port)
    if valid_port is False:
        print err
        sys.exit()

    server = server.Server(int(server_port))
    server.main_loop()
