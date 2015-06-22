import struct
import hashlib

# https://docs.python.org/2/library/struct.html#format-characters
FORMAT_STR = '!LLLh32s?????'

class Header:
    def __init__(self, seqn, ackn, ftp_pos, window_size, checksum, syn=False, ack=False, fin=False, file_name=False, ftp=False):
        self.seqn = seqn                                             #  4 bytes
        self.ackn = ackn                                             #  4 bytes
        self.window_size = window_size                               #  2 bytes
        self.checksum = checksum                                     # 32 bytes
        self.ftp_pos = ftp_pos
        self.flags = [syn, ack, fin, file_name, ftp]                      #  4 bytes
        self.syn = syn
        self.ack = ack
        self.fin = fin
        self.ftp = ftp
        self.file_name = file_name
        self.formatted = struct.pack(FORMAT_STR, self.seqn, self.ackn, self.ftp_pos, self.window_size, self.checksum, *self.flags)

    @staticmethod
    def parse(header):
        unpacked = struct.unpack(FORMAT_STR, header)
        return Header(*unpacked)

    @staticmethod
    def size():
        return 51

    @staticmethod
    def checksum(data):
        return hashlib.md5(data).hexdigest()
