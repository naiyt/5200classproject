from interface import Interface
from marshaller import Marshal

class MethodImplementations(Interface):
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

class Server:
    def __init__(self):
        self.methods = MethodImplementations()
        self._register_methods()
        self.marshal = Marshal()

    def receive(self):
        data = ('add', 1, 1)
        return self._call(data[0], *data[1:])

    def _unmarshal(self, data):
        return self.marshal.unmarshal(data)

    def _call(self, meth_name, *args):
        return self.method_impls[meth_name](*args)

    def _send(result):
        marshalled = self.marshal.marshal(result)
        print 'sending result'

    def _register_methods(self):
        methods = [x for x in dir(MethodImplementations) if x[0:1] != '_']
        self.method_impls = {}
        for method in methods:
            self.method_impls[method] = getattr(self.methods, method)

server = Server()
print server.receive()
