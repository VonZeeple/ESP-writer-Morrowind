from ctypes import c_longlong as ll


def get_formated_string(string, length):
    if length is None:
        return string+'\0'
    if len(string) > length:
        return string[0:length]
    elif len(string) <= length:
        return string + chr(0)*(length - len(string))

def get_type_str(var):
    if isinstance(var, str):
        return str(len(var)) + 's'
    elif isinstance(var, (long, int)):
        return 'l'
    elif isinstance(var, float):
        return 'f'
    elif isinstance(var, ll):
        return 'q'
    elif isinstance(var, chr):
        return 'c'
    else:
        return None

