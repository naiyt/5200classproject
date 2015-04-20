class Interface:
    def __init__(self):
        self.req_ids = { 'add': 1, 'subtract': 2 }

    def add(self, a, b):
        raise NotImplementedError()

    def subtract(self, a, b):
        raise NotImplementedError()
