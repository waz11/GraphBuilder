from GraphBuilder.Components.ClassAttribute import ClassAttribute


class MultiTypeClassAttribute(ClassAttribute):
    def __init__(self, class_task, attribute_name, att_types, object_type):
        super().__init__(class_task, attribute_name, object_type=object_type)
        self.types = att_types