import struct
import hashlib

# https://docs.python.org/2/library/struct.html#format-characters
FORMAT_STR = '!LLh32s????'

class Header:
    def __init__(self, seqn, ackn, window_size, data, syn=False, ack=False, fin=False, file_name=False):
        self.seqn = seqn                                             #  4 bytes
        self.ackn = ackn                                             #  4 bytes
        self.window_size = window_size                               #  2 bytes
        self.checksum = Header.checksum(data)                        # 32 bytes
        self.flags = [syn, ack, fin, file_name]                      #  4 bytes
        self.formatted = struct.pack(FORMAT_STR, self.seqn, self.ackn, self.window_size, self.checksum, *self.flags)

    @staticmethod
    def parse(header):
        unpacked = struct.unpack(FORMAT_STR, header)
        return Header(*unpacked)

    @staticmethod
    def size():
        return 46

    @staticmethod
    def checksum(data):
        return hashlib.md5(data).hexdigest()
