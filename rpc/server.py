from marshaller import Marshal
from reliable_transport import server
from reliable_transport import client
from method_implementations import MethodImplementations

class Server:
    def __init__(self, port, address):
        self.methods = MethodImplementations()
        self._register_methods()
        self.marshal = Marshal()
        self.server = server.Server(port)
        self.client = client.Client(address, port+10)

    def receive(self):
        data = self.server.receive_loop()
        unmarshalled = self._unmarshal(data)
        args = self._set_arg_types(unmarshalled['args'], unmarshalled['sig'])
        return self._call(unmarshalled['name'], *args), unmarshalled

    def send(self, result, um):
        marshalled = self.marshal.marshal(um['name'], um['id'], um['sig'], um['args'], result)
        print marshalled
        self.client.transmit_data(marshalled)

    def _set_arg_types(self, args, sig):
        typed_args = []
        for i in range(0, len(args)):
            if sig[i] == 'int':
                new_arg = int(args[i])
            elif sig[i] == 'float':
                new_arg = int(args[i])
            elif sig[i] == 'bool':
                new_arg = bool(args[i])
            elif sig[i] == 'str':
                new_arg = args[i]
            typed_args.append(new_arg)
        return typed_args

    def _unmarshal(self, data):
        return self.marshal.unmarshal(data)

    def _call(self, meth_name, *args):
        return self.method_impls[meth_name](*args)

    def _register_methods(self):
        methods = [x for x in dir(MethodImplementations) if x[0:1] != '_']
        self.method_impls = {}
        for method in methods:
            self.method_impls[method] = getattr(self.methods, method)

server = Server(1234, 'localhost')

while True:
    result, unmarshalled = server.receive()
    server.send(result, unmarshalled)
