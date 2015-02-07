{"filter":false,"title":"udpserver.py","tooltip":"/udp/udpserver.py","undoManager":{"mark":1,"position":1,"stack":[[{"group":"doc","deltas":[{"start":{"row":0,"column":0},"end":{"row":53,"column":3},"action":"insert","lines":["import socket","","class UdpServer:","    def __init__(self, port, num_connections=5):","        self.serv_sock = socket.socket()","        self.host = socket.gethostname()","        self.port = port","        self.serv_sock.bind((self.host, self.port))","        self.serv_sock.listen(num_connections)","                ","","","def main_loop(server):","\twhile True:","\t\tclnt_sock, addr = server.serv_sock.accept()","\t\tclnt_sock.send(\"Connected\")","\t\tclnt_sock.close()","    ","","","","\"\"\"","import socket","","## 1. construct a server socket object","serv_sock = socket.socket()","","## 2. get the hostname","host = socket.gethostname()","print 'host:', host","## 3. set the port number","port = 1234","print 'port:', port","","## 4. bind the socket to the host","##    and the port","serv_sock.bind((host, port))","","## 5. specify the number of connections","##    that can be queued up on the","##    socket.","serv_sock.listen(5)","","## 6. go into infinite loop","while True:","    ## 6.1. accept connections","    clnt_sock, addr = serv_sock.accept()","    ## 6.2. print the address of the connection","    print 'Got connection from', addr","    ## 6.3. send a simple string","    clnt_sock.send('Thank you for connecting')","    ## 6.4 close the connection","    clnt_sock.close()","\"\"\""]}]}],[{"group":"doc","deltas":[{"start":{"row":10,"column":0},"end":{"row":17,"column":4},"action":"remove","lines":["","","def main_loop(server):","\twhile True:","\t\tclnt_sock, addr = server.serv_sock.accept()","\t\tclnt_sock.send(\"Connected\")","\t\tclnt_sock.close()","    "]}]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":17,"column":38},"end":{"row":17,"column":38},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1422486431509,"hash":"6a193705f654277542e8608de99d51bcfcac3fa5"}