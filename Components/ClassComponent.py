from Components.Component import Component


class ClassComponent(Component):

    def __init__(self, class_name):
        super().__init__()
        self.class_name = class_name
        self.Attributes = []
        self.Methods = []
        self.Implements = []
        self.Extends = None
        self.Constructors = []
        self.sub_classes = []
        self.Enums = []

    def get_class_atts_names(self):
        att_names = []
        for att in self.Attributes:
            curr_att_dec = att.name
            if att.att_type is not None and att.att_type.class_name is not None:
                curr_att_dec = att.att_type.class_name + " " + curr_att_dec
            att_names.append(curr_att_dec)
        return att_names

    def add_sub_class(self, sub_class):
        self.sub_classes.append(sub_class)

    def add_class_enums(self, enum):
        self.Enums.append(enum)

    def add_implement_class(self, implement_class):
        self.Implements.append(implement_class)

    def add_extended_class(self, extended_class):
        self.Extends = extended_class

    def add_constructors(self, constructor):
        self.Constructors.append(constructor)

    def add_class_methods(self, method):
        self.Methods.append(method)

    def add_class_attributes(self, attribute):
        self.Attributes.append(attribute)

    def get_class_object(self):
        return self.task

    def get_class_name(self):
        return self.class_name

    def get_class_attributes(self):
        return self.Attributes

    def get_class_method(self, method):
        return next((x for x in self.Methods if x.get_method_name() == method), None)

    def get_specific_attribute(self, attribute):
        return next((x for x in self.Attributes if x.get_attribute_name() == attribute), None)

    def get_all_method(self):
        return self.Methods

    def get_constructor(self):
        if self.Constructors:
            return self.Constructors[0]
        return None

    def __eq__(self, other):
        return self.class_name == other.get_class_name()