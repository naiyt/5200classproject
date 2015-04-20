import struct

class Marshal:
    def __init__(self):
        pass

    def _format_sig(self, signature):
        format_str = '!'
        for t in signature:
            if t is int:
                format_str += 'i'
            if t is long:
                format_str += 'L'
            if t is float:
                format_str += 'f'
            if t is str:
                format_str += "{}s".format(len(arg))
            if t is bool:
                format_str += '?'
        return format_str

    def marshal(self, req_id, signature, args):
        format_str = self._format_sig(signature)
        return struct.pack(format_str, 1, 2)

    def unmarshal(self, data):
        return data
