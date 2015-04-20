import struct

class Marshal:
    def __init__(self):
        pass

    def marshal(self, req_id, args):
        format_str = '!'
        for arg in args:
            if isinstance(arg, int):
                format_str += 'i'
            if isinstance(arg, long):
                format_str += 'L'
            if isinstance(arg, float):
                format_str += 'f'
            if isinstance(arg, str):
                format_str += "{}s".format(len(arg))
            if isinstance(arg, bool):
                format_str += '?'
        return struct.pack(format_str, 1, 2)

    def unmarshal(self, data):
        return data
