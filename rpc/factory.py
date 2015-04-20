from proxy import Proxy

class Factory:
    def __init__(self):
        self.proxy = None

    def get_proxy(self):
        if self.proxy is None:
            self.proxy = Proxy('localhost', 9999)
        return self.proxy
