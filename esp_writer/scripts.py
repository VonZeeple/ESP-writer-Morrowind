# coding=utf8
from esp_writer.records import *

class script:
    def __init__(self, script_name, shorts=[], longs=[],floats=[]):
        self.name = script_name
        self.shorts = shorts
        self.longs = longs
        self.floats = floats
        self.size = None
        self.text = ''

    def get_SCVR(self):
        s = ''
        for var in self.shorts+self.longs+self.floats:
            s += var+'\0'
        return SubRecord('SCVR', utils.get_formated_string(s, None))
