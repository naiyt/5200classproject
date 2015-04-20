from interface import Interface
from marshaller import Marshal

class Proxy(Interface):
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.marshaller = Marshal()
        Interface.__init__(self)

    def connect(self):
        print 'TODO: connect should connect to the remote server via reliable transport'

    def add(self, a, b):
        return self._get_remote_answer('add', a, b)

    def subtract(self, a, b):
        return self._get_remote_answer('subtract', a, b)

    def _get_remote_answer(self, meth_name, *args):
        marshalled = self.marshaller.marshal(self.req_ids[meth_name], args)
        data = self._transmit(marshalled)
        return self.marshaller.unmarshal(data)

    def _transmit(self, data):
        print 'TODO: _transmit should transmit and receive the data back'
        return "3"
