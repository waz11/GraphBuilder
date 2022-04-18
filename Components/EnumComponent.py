from Components.Component import Component


class EnumComponent(Component):
    def __init__(self, enum_name, task):
        super().__init__()
        self.enum_name = enum_name
        self.super_task = task
        self.enum_consts = []

    def add_enum_const(self, const):
        self.enum_consts.append(const)