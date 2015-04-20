class Interface:
    def __init__(self):
        methods = [x for x in dir(Interface) if x[0:1] != '_']
        self.req_ids = {}
        num = 0
        for method in methods:
            self.req_ids[method] = num
            num += 1
        print self.req_ids

    def add(self, a, b):
        raise NotImplementedError()

    def subtract(self, a, b):
        raise NotImplementedError()
