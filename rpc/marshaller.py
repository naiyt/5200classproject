class Marshal:
    def __init__(self):
        pass

    def marshal(self, name, req_id, signature, args):
        sig = ','.join(signature)
        args = ','.join([str(x) for x in args])
        return ';'.join([name, sig, args, str(req_id)])

    def unmarshal(self, data):
        unmarshalled = data.split(';')
        name = unmarshalled[0]
        sig = unmarshalled[1].split(',')
        args = unmarshalled[2].split(',')
        id = unmarshalled[3]
        result = unmarshalled[4]
        return { 'name': name, 'sig': sig, 'args': args, 'id': id, result: 'result' }

# Marshal example: add(1, 2) -> "add;int,int;1,2;req_id;result"
# "func_name;type,type;param,param;request_id;result" <- result is null on the client
# str[0] = name, str[1] = signature, str[2] = parameters, str[3] = id, str[4] = result