import socket

class UdpClient:
    def __init__(self, host, port, tcp=False):
        self.host = host
        self.port = port
        if tcp:
            self.clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.clnt_sock = socket.socket()
        
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
