import inspect
import random
import sys
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
        self._init_funcs()
        self.req_id = random.randint(1, sys.maxint)

    def connect(self):
        self.client = client.Client(self.address, self.port)
        self.server = server.Server(self.port+10)

    def get_remote_answer(self, meth_name, signature, req_id, *args):
        marshalled = self.marshaller.marshal(meth_name, req_id, signature, *args)
        data = self._transmit(marshalled)
        return self.marshaller.unmarshal(data)['result']

    def _transmit(self, data):
        self.client.transmit_data(data)
        return self.server.receive_loop()

    def _init_funcs(self):
        stubs = {}
        for name, method in self.methods.iteritems():
            stubs[name] = Stub(name,  method['sig'], method['return'], self)
            setattr(self, name, stubs[name].create_stub)

class Stub:
    def __init__(self, method_name, signature, return_type, proxy):
        self.method_name = method_name
        self.signature = signature
        self.proxy = proxy
        self.return_type = return_type

    def create_stub(self, *args):
        self.args = args
        self.proxy.req_id = self.proxy.req_id + 1 % sys.maxint
        self.req_id = self.proxy.req_id
        return self.receive_answer()

    def receive_answer(self):
        answer = self.proxy.get_remote_answer(self.method_name, self.signature, self.req_id, self.args)
        if self.return_type == 'int':
            answer = int(answer)
        elif self.return_type == 'float':
            answer = int(answer)
        elif self.return_type == 'bool':
            answer = bool(answer)
        return answer
