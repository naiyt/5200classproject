class MethodImplementations(Interface):
    def add(a, b):
        return a + b

    def subtract(a, b):
        return a - b

class Server:
    def __init__(self):
        self.methods = MethodImplementations()
        self.skeleton = Stub()
        self.marshal = Marshal()

    def receive():
        print 'receiving data'

    def _unmarshal(data):
        return self.marshal.unmarshal(data)

    def _call(meth_name, args):
        return self.methods.meth_name(*args)

    def _send(result):
        marshalled = self.marshal.marshal(result)
        print 'sending result'
