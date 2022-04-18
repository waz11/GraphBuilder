from Components.Component import Component


class ClassAttribute(Component):

    def __init__(self, class_task, attribute_name, att_type=None, object_type=None):
        super().__init__()
        self.class_name = class_task
        self.name = attribute_name
        self.att_type = att_type
        self.object_type = object_type

    def get_att_obj_type(self):
        return self.object_type

    def get_attribute_name(self):
        return self.name

    def get_attribute_class(self):
        return self.class_name

    def get_attribute_type(self):
        return self.att_type