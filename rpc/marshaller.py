class Marshal:
    def __init__(self):
        pass

    def marshal(self, req_id, *args):
        return "{} {}".format(req_id, args)

    def unmarshal(self, data):
        return data
