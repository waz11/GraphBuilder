from Components.Component import Component
from Parser import codeExtractor


class CodeWrapper(Component):
    def __init__(self, query, text):
        super().__init__()
        self.query = query
        self.text = text
        self.answer_text = None
        self.sub_classes = []
        self.url = None
        self.methods = []
        self.imports = []
        self.imports_codes = []
        self.tags = []
        self.score = None
        self.post_id = None

    def __eq__(self, other):
        if self.query == other.query:
            return True
        return False

    def set_id(self, post_id):
        self.post_id = post_id

    def set_tags(self, tags):
        self.tags = tags

    def set_score(self, score):
        self.score = score

    def set_url(self, url):
        self.url = url

    def get_queries_class(self):
        return self.sub_classes

    def get_class(self, class_to_return):
        for curr_class in self.sub_classes:
            if curr_class.get_class_name() in codeExtractor.primitive_types:
                continue
            else:
                if curr_class.get_class_name() == class_to_return:
                    return curr_class
        return None

    def get_methods(self, method_name):
        return next((x for x in self.methods if x.get_method_name() == method_name), None)

    def add_imports(self, _import):
        self.imports.append(_import)

    def add_answer_text(self, answer_text):
        self.text += answer_text

    def add_methods(self, method):
        self.methods.append(method)

    def add_class(self, task):
        self.sub_classes.append(task)

    def add_imports_code(self, _import):
        self.imports_codes.append(_import)