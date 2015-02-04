import socket

class UdpClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clnt_sock = socket.socket()
        
    def connect(self):
        self.clnt_sock.connect((self.host, self.port))

    def transmit(self, filename):
        print "TODO: add code to transmit file"
        #open file
        #create byte buffer for transmission
        #send filename to server
        #For loop
        #determine if end of file is reached
        #read upto 500 bytes of file, keeping track of current position in file
        #write bytes to send buffer
        #send 500 byte buffer
        #end For loop
        #send end of file message