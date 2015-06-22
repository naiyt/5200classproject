class Marshal:
    def __init__(self):
        pass

    def marshal(self, name, req_id, signature, args, result=None):
        sig = ','.join(signature)
        args = ','.join([str(x) for x in args])
        return ';'.join([name, sig, args, str(req_id), str(result)])

    def unmarshal(self, data):
        unmarshalled = data.split(';')
        name = unmarshalled[0]
        sig = unmarshalled[1].split(',')
        args = unmarshalled[2].split(',')
        id = unmarshalled[3]
        if len(unmarshalled) == 5:
            result = unmarshalled[4]
            return { 'name': name, 'sig': sig, 'args': args, 'id': id, 'result': result }
        else:
            return { 'name': name, 'sig': sig, 'args': args, 'id': id }
