import inspect
from interface import Interface
from marshaller import Marshal
from reliable_transport import client
from reliable_transport import server

class Proxy(Interface):
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.marshaller = Marshal()
        self._create_stubs()
        Interface.__init__(self)

    def connect(self):
        self.client = client.Client(self.address, self.port)
        self.server = server.Server(self.port+10)

    def get_remote_answer(self, meth_name, *args):
        marshalled = self.marshaller.marshal(self.req_ids[meth_name], *args)
        data = self._transmit(marshalled)
        return self.marshaller.unmarshal(data)

    def _transmit(self, data):
        self.client.transmit_data(data)
        return server.receive_loop()

    def _create_stubs(self):
        stubs = {}
        methods = [x for x in dir(Interface) if x[0:2] != '__']
        for method in methods:
            stubs[method] = Stub(method, self)
            setattr(self, method, stubs[method].receive_answer)

class Stub:
    def __init__(self, method_name, proxy):
        self.method_name = method_name
        self.proxy = proxy

    def receive_answer(self, *args):
        return self.proxy.get_remote_answer(self.method_name, args)
