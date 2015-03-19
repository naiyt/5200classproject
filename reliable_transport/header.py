import struct
import hashlib

# https://docs.python.org/2/library/struct.html#format-characters
FORMAT_STR = '!LLhh32s'

class Header:
    def __init__(self, seqn, ackn, window_size, flags, data):
        self.seqn = seqn                        #  4 bytes
        self.ackn = ackn                        #  4 bytes
        self.window_size = window_size          #  2 bytes
        self.flags = flags                      #  2 bytes
        self.checksum = Header.checksum(data)   # 32 bytes
        self.formatted = struct.pack(FORMAT_STR, self.seqn, self.ackn, self.window_size, self.flags, self.checksum)

    @staticmethod
    def parse(header):
        unpacked = struct.unpack(FORMAT_STR, header)
        return Header(unpacked[0], unpacked[1], unpacked[2], unpacked[3])

    @staticmethod
    def size():
        return 44

    @staticmethod
    def checksum(data):
        return hashlib.md5(data).hexdigest()
