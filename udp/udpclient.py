import socket

class UdpClient:
    def __init__(self, host, port, tcp=False):
        self.host = host
        self.port = port
        protocol = socket.SOCK_STREAM if tcp else socket.SOCK_DGRAM
        self.clnt_sock = socket.socket(socket.AF_INET, protocl)
        
    def connect(self):
        self.clnt_sock.connect((self.host, self.port))

    def transmitFile(self, filename):
        self.clnt_sock.send(filename)
        self.clnt_sock.recv(500)
        with open(filename, 'r') as f:
            while True:
                byte_s = f.read(500)
                if not byte_s:
                    break
                self.clnt_sock.send(byte_s)
        self.clnt_sock.send("")
