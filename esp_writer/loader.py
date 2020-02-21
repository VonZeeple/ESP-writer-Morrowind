import struct
from records import *

def get_esm_size(filename):
    f = open(filename, 'rb')
    print len(f.read())
    f.close()

def loadESP(filename):
    records=[]
    f = open(filename, 'rb')
    bytes_left = len(f.read())
    print bytes_left
    f.seek(0)
    while bytes_left > 0:
        record, size = load_record(f)
        bytes_left -= size
        records.append(record)
    f.close()
    return records


def load_sub_record(data_in):
    name = struct.unpack('4s', data_in[0:4])[0]
    size = struct.unpack('l', data_in[4:8])[0]
    data = data_in[8:8 + size]
    subrecord = SubRecord(name, data)
    return subrecord, size + 8


def load_sub_records(data_in, size_in):
    sub_records = []
    bytes_left = size_in
    while bytes_left >= 1:
        sub_record, size = load_sub_record(data_in[-bytes_left::])
        bytes_left -= size
        sub_records.append(sub_record)
    return sub_records

def load_record(input_file):
    name = struct.unpack('4s', input_file.read(4))[0]
    size = struct.unpack('l', input_file.read(4))[0]  # size of the record
    header1 = struct.unpack('l', input_file.read(4))[0]  # Header1
    flag = struct.unpack('l', input_file.read(4))[0]  # Flags
    data = input_file.read(size)
    sub_records = load_sub_records(data, size)
    record = Record(name, header1=header1, flag=flag, sub_records=sub_records)
    return record, size + 16


