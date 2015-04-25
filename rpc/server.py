from interface import Interface
from marshaller import Marshal
from reliable_transport import server
from reliable_transport import client

class MethodImplementations(Interface):
    def add(a, b):
        return a + b

    def subtract(a, b):
        return a - b

class Server:
    def __init__(self, port, address):
        self.methods = MethodImplementations()
        self._register_methods()
        self.marshal = Marshal()
        self.server = server.Server(port)
        self.client = client.Client(address, port+10)

    def receive(self):
        data = self.server.receive_loop()
        data = self._unmarshal(data)
        # data = ('add', 1, 1)
        return self._call(data[0], *data[1:]) # data[0] is the func, the rest of the arr is the args

    def _unmarshal(self, data):
        return self.marshal.unmarshal(data)

    def _call(self, meth_name, *args):
        return self.method_impls[meth_name](*args)

    def _send(result):
        marshalled = self.marshal.marshal(result)
        self.client.transmit_data(marshalled)

    def _register_methods(self):
        methods = [x for x in dir(MethodImplementations) if x[0:1] != '_']
        self.method_impls = {}
        for method in methods:
            self.method_impls[method] = getattr(self.methods, method)

server = Server(1234, 'localhost')
server.receive()
