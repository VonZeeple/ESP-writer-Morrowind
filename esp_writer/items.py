class MiscItem:
    def __init__(self, id, name, model_fn, **kwargs):
        self.id = id
        self.name = name
        self.model = model_fn
        self.weight = kwargs.get('weight', 0)
        self.value = kwargs.get('value', 0)
        self.unknown = 0L
        self.icon = kwargs.get('icon', None)
        self.ench_str = kwargs.get('ench_str', None)
        self.script_str = kwargs.get('script_str', None)

    def get_record(self):
        pass


class Weapon(MiscItem):
    def __init__(self):
        pass

