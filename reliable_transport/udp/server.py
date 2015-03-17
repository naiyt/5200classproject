import socket

class Server:
    def __init__(self, port, tcp=False, num_connections=5, packet_size=500):
        self.tcp = tcp
        self.packet_size = packet_size
        protocol = socket.SOCK_STREAM if tcp else socket.SOCK_DGRAM
        self.serv_sock = socket.socket(socket.AF_INET, protocol)
        self.host = socket.gethostname()
        self.port = port
        self.serv_sock.bind((self.host, self.port))
        if self.tcp:
          self.serv_sock.listen(num_connections)

    def begin(self):
      if self.tcp:
        self.clnt_sock, _ = self.serv_sock.accept()
      else:
        self.clnt_sock = self.serv_sock

    def recv(self):
      if self.tcp:
        return self.clnt_sock.recv(self.packet_size)
      else:
        data = self.clnt_sock.recvfrom(self.packet_size) # With udp, it returns a tuple, where the first entry is the data, second is the ip received from
        return data[0]

    def ack(self):
      if self.tcp:
        self.clnt_sock.send("ACKNOWLEDGED")

    def close(self):
      if self.tcp:
        self.clnt_sock.close()
