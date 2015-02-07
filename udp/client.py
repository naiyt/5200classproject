import socket

class Client:
    def __init__(self, host, port, tcp=False, packet_size=500):
        self.tcp = tcp
        self.packet_size = packet_size
        self.host = host
        self.port = port
        protocol = socket.SOCK_STREAM if tcp else socket.SOCK_DGRAM
        self.clnt_sock = socket.socket(socket.AF_INET, protocol)
        
    def connect(self):
        if self.tcp:
            self.clnt_sock.connect((self.host, self.port))

    def transmitFile(self, filename):
        self.send(filename)

        if self.tcp:
            self.clnt_sock.recv(500)

        with open(filename, 'r') as f:
            while True:
                byte_s = f.read(500)
                if not byte_s:
                    break
                self.send(byte_s)
        self.send("")

    def send(self, to_send):
        if self.tcp:
            self.clnt_sock.send(to_send)
        else:
            self.clnt_sock.sendto(to_send, (self.host, self.port))
