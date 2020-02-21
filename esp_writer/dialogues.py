# coding=utf8
from esp_writer.records import *
import esp_writer.utils
import random


def get_info_id():
    return random.randint(0, 2**32-1)

class Topic:
    def __init__(self, text='', dialogue_type='regular'):
        self.text = text
        self.dialogue_type = dialogue_type
        self.infos = []

    def get_record(self):
        topic_indexes = {'regular': 0, 'voice': 1, 'greetings': 2, 'persuasion': 3, 'journal': 4}
        records = []
        topic_record = Record('DIAL')
        topic_record.sub_records.append(SubRecord('NAME', utils.get_formated_string(self.text, None)))
        topic_record.sub_records.append(SubRecord('DATA', chr(topic_indexes.get(self.dialogue_type, 0))))
        records.append(topic_record)
        for t in self.infos:
            records.append(t.get_record())
        return records

    def add_info(self, info):
        self.infos.append(info)
        if len(self.infos) > 1:
            self.infos[-2].nnam = self.infos[-1].inam
            self.infos[-1].pnam = self.infos[-2].inam


class Condition:
    def __init__(self, typ, code, comp_op, result):
        self.typ = str(typ)
        self.comp_op = str(comp_op)
        self.name = str(code)
        self.result = int(result)

    def get_cond_records(self, index):
        types = {'nothing': 0, 'function': 1, 'global': 2, 'local': 3, 'journal': 4, 'item': 5,
             'dead': 6, 'not id': 7, 'not faction': 8, 'not class': 9, 'not race': 10, 'not cell': 11, 'not local': 12}
        functions = {'nothing': '\\xFF', 'function': '\\xFF', 'global': 'sX', 'local': 'sX', 'journal': 'JX', 'item': 'IX',
             'dead': 'DX', 'not id': 'XX', 'not faction': 'FX', 'not class': 'CX', 'not race': 'RX', 'not cell': 'LX',
                 'not local': 'sX'}
        operators = {'=': 0, '!=': 1, '>': 2, '>=': 3, '<': 4, '<=': 5}

        s = str(index)+str(types[self.typ])

        if self.typ == 'function':
            s += str(function_code[self.name])
        else:
            s += str(functions.get(self.typ, '\\xFF'))

        s += str(operators.get(self.comp_op, '\\xFF'))
        if self.typ != 'function':
            s += self.name
        scvr = SubRecord('SCVR', data=[s])
        if isinstance(self.result, float):
            fltv = SubRecord('FLTV', data=[int(self.result)])
        else:
            fltv = SubRecord('INTV', data=[int(self.result)])
        return [scvr, fltv]


def unpack_info(record):
        out = {}
        for sub in record.sub_records:
            if sub.name in out:
                if type(out[sub.name]) is list:
                    out[sub.name].append(sub.data)
                else:
                    out[sub.name] = [out[sub.name], sub.data]
            else:
                out[sub.name] = sub.data
        return out

class Info:
    def __init__(self, inam, text, pnam=None, nnam=None, **kwargs):
        self.name = text
        self.pnam = pnam
        self.inam = inam
        self.nnam = nnam

        self.unknown1 = 0
        self.disposition = kwargs.get('disposition', 0)
        self.rank = kwargs.get('rank', 0xFF)
        self.pc_rank = kwargs.get('pc_rank', 0xFF)
        self.gender = kwargs.get('gender', 'none')
        self.unknown2 = 0
        self.conditions = []
        self.actor_str = kwargs.get('actor', None)
        self.race_str = kwargs.get('race', None)
        self.class_str = kwargs.get('class', None)
        self.faction_str = kwargs.get('faction', None)
        self.cell_str = kwargs.get('cell', None)
        self.pcfaction_str = kwargs.get('pc faction', None)
        self.sound = kwargs.get('sound', None)
        self.result_text = kwargs.get('result text', '')



    def get_record(self):
        genders = {'none': 0xFF, 'female': 1, 'male': 0}

        info = Record('INFO')
        def append_to_info(name, var):
            if var is not None:
                info.sub_records.append(SubRecord(name, utils.get_formated_string(var, None)))

        #info.sub_records.append(SubRecord('INAM', utils.get_formated_string(str(self.inam), None)))
        append_to_info('INAM', str(self.inam))
        append_to_info('PNAM', str(self.pnam))
        append_to_info('NNAM', str(self.nnam))

        data = [self.unknown1, self.disposition, chr(self.rank), chr(genders.get(self.gender, genders['none'])), chr(self.pc_rank), chr(self.unknown2)]
        info.sub_records.append(SubRecord('DATA', data))

        append_to_info('ONAM',  self.actor_str)
        append_to_info('RNAM',  self.race_str)
        append_to_info('CNAM',  self.class_str)
        append_to_info('FNAM',  self.faction_str)
        append_to_info('ANAM',  self.cell_str)
        append_to_info('DNAM',  self.pcfaction_str)
        info.sub_records.append(SubRecord('NAME', self.name))
        append_to_info('SNAM', self.sound)
        for i, c in enumerate(self.conditions):
            info.sub_records.append(c.get_cond_records(i)[0])
            info.sub_records.append(c.get_cond_records(i)[1])

        append_to_info('BNAM', self.result_text)
        return info

function_code= {
    'Rank Low': '00',
    'Ranck High': '01',
    'Rank Requirement': '02',
    'Reputation': '03',
    'Health Percent': '04',
    'PC Reputation': '05',
    'PC Level': '06',
    'PC Health Percent': '07',
    'PC Magicka': '08',
    'PC Fatigue': '09',
    'PC Strength': '10',
    'PC Block': '11',
    'PC Armorer': '12',
    'PC Medium Armor': '13',
    'PC Heavy Armor': '14',
    'PC Blunt Weapon': '15',
    'PC Long Blade': '16',
    'PC Axe': '17',
    'PC Spear': '18',
    'PC Athletics': '19',
    'PC Enchant': '20',
    'PC Destruction': '21',
    'PC Alteration': '22',
    'PC Illusion': '23',
    'PC Conjuration': '24',
    'PC Mysticism': '25',
    'PC Restoration': '26',
    'PC Alchemy': '27',
    'PC Unarmored': '28',
    'PC Security': '29',
    'PC Sneak': '30',
    'PC Acrobatics': '31',
    'PC Light Armor': '32',
    'PC Short Blade': '33',
    'PC Marksman': '34',
    'PC Mercantile': '35',
    'PC Speechcraft': '36',
    'PC Hand-to-Hand': '37',
    'PC Gender': '38',
    'PC Expelled': '39',
    'PC Common Disease': '40',
    'PC Blight Disease': '41',
    'PC Clothing Modifier': '42',
    'PC Crime Level': '43',
    'Same Gender': '44',
    'Same Race': '45',
    'Same Faction': '46',
    'Faction Rank Diff': '47',
    'Detected': '48',
    'Alarmed?': '49',
    'Choice': '50',
    'PC Intelligence': '51',
    'PC Willpower': '52',
    'PC Agility': '53',
    'PC Speed': '54',
    'PC Endurance': '55',
    'PC Personality': '56',
    'PC Luck': '57',
    'PC Corprus': '58',
    'Weather': '59',
    'PC Vampire': '60',
    'Level': '61',
    'Attacked': '62',
    'Talked to PC': '63',
    'PC Health': '64',
    'Creature Target': '65',
    'Friend Hit': '66',
    'Fight': '67',
    'Hello': '68',
    'Alarm': '69',
    'Flee': '70',
    'Should Attack': '71'
}
