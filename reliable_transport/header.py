import struct

FORMAT_STR = '!LLhh'

class Header:
    def __init__(self, seqn, ackn, window_size, flags):
        self.seqn = seqn
        self.ackn = ackn
        self.window_size = window_size
        self.flags = flags
        self.formatted = struct.pack(FORMAT_STR, self.seqn, self.ackn, self.window_size, self.flags)

    @staticmethod
    def parse(header):
        unpacked = struct.unpack(FORMAT_STR, header)
        return Header(unpacked[0], unpacked[1], unpacked[2], unpacked[3])

    @staticmethod
    def size():
        return 12
