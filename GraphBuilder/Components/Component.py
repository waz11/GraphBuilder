class Component:

    def __init__(self):
        self.task = None
        self.key = 0
        self.documentation = ""
        self.code = None
        self.code_changed = False

    def changed_code(self):
        self.code_changed = True

    def get_key(self):
        return self.key

    def set_documentation(self, documentation):
        documentation = documentation.replace("/**", '')
        documentation = documentation.replace("*/", '')
        self.documentation += documentation

    def set_key(self, key):
        self.key = key

    def set_code(self, code):
        if self.code is not None:
            self.code_changed = True
        self.code = code