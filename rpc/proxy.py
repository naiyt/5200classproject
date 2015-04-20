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
        Interface.__init__(self)
        self._create_stubs()

    def connect(self):
        self.client = client.Client(self.address, self.port)
        self.server = server.Server(self.port+10)

    def get_remote_answer(self, meth_name, req_id, signature, *args):
        marshalled = self.marshaller.marshal(req_id, signature, *args)
        data = self._transmit(marshalled)
        return self.marshaller.unmarshal(data)

    def _transmit(self, data):
        self.client.transmit_data(data)
        return server.receive_loop()

    def _create_stubs(self):
        stubs = {}
        for name, method in self.methods.iteritems():
            stubs[name] = Stub(name, method['id'], method['sig'], self)
            setattr(self, name, stubs[name].receive_answer)

class Stub:
    def __init__(self, method_name, req_id, signature, proxy):
        self.method_name = method_name
        self.req_id = req_id
        self.signature = signature
        self.proxy = proxy

    def receive_answer(self, *args):
        return self.proxy.get_remote_answer(self.method_name, self.req_id, self.signature, args)
