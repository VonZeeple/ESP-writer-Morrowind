# coding=utf8
import struct
import esp_writer.utils as utils
from ctypes import c_longlong as ll


class SubRecord:
    def __init__(self, name, data=[]):
        self.name = name
        self.data = data


    def pack(self):
        s = ''
        for e in self.data:
            if isinstance(e, ll):
                s += struct.pack('q', e.value)
            else:
                s += struct.pack(utils.get_type_str(e), e)
        size = len(s)
        #print self.name
        return struct.pack('4s', self.name)+struct.pack('l', size) + s

    def __str__(self):
        return self.name+': '+str(self.data)


class Record:
    def __init__(self, name, header1=0, flag=0):
        self.name = name
        self.header1 = header1
        self.flag = flag
        self.sub_records = []

    def pack(self):
        s = ''
        for sr in self.sub_records:
            s += sr.pack()
        size = len(s)
        return struct.pack('4s', self.name) + struct.pack('l', size) + struct.pack('l', self.header1) + struct.pack('l', self.flag) + s

