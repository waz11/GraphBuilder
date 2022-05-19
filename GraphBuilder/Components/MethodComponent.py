from GraphBuilder.Components.Component import Component


class MethodComponent(Component):

    def __init__(self, method_name, class_task):
        super().__init__()
        self.task = class_task
        self.Attributes = []
        self.method_name = method_name
        self.calling_methods = []
        self.method_token = None
        self.params = []

    def add_method_calls(self, method):
        self.calling_methods.append(method)

    def add_method_attributes(self, attribute):
        self.Attributes.append(attribute)

    def get_method_name(self):
        return self.method_name

    def get_method_super_class(self):
        return self.task

    def get_calling_method(self):
        return self.calling_methods

    def get_attribute(self, attribute):
        return next((x for x in self.Attributes if x.get_attribute_name() == attribute), None)

    def find_method_call(self, method_called):
        for calling in self.calling_methods:
            if calling.get_method_name() == method_called:
                return calling
        return None
