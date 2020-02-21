# coding=utf8

from esp_writer.records import *
from ctypes import c_longlong as ll
import esp_writer.utils


class Root:
    def __init__(self):
        self.records =[MainHeader()]

    def register(self, object):
        self.records.append(object)

    def compile(self):
        pass
        #mettre a jour le nombre de records dans le header


class MainHeader:
    def __init__(self):
        self.version = 1.0
        self.unknown_long = 0L#Change de master file (1L) a pluging (0L)
        self.author = 'VZ'
        self.description = 'description of the mod'
        self.master_files = [('Morrowind.esm', 80681814), ('Tribunal.esm', 4697358), ('Bloodmoon.esm', 10015689)]
        self.num_records = 0

    def get_record(self):
        hedr_data = [self.version, self.unknown_long,
                     utils.get_formated_string(self.author, 32),
                     utils.get_formated_string(self.description, 256),
                     self.num_records]
        tes3 = Record('TES3')
        tes3.sub_records.append(SubRecord('HEDR', data=hedr_data))
        for m in self.master_files:
            tes3.sub_records.append(SubRecord('MAST', data=[utils.get_formated_string(m[0], None)]))
            tes3.sub_records.append(SubRecord('DATA', data=[ll(m[1])]))
        return tes3

