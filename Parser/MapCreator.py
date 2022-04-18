
def handle_vertex(mapped_dict, name, key, **kwargs):
    mapped_dict["name"] = name
    mapped_dict["key"] = key
    if "type" in kwargs and kwargs["type"]:
        mapped_dict["type"] = kwargs["type"]
    if "att_names" in kwargs and kwargs["att_names"]:
        mapped_dict["attributes"] = kwargs["att_names"]


def handle_edge(mapped_arrows_dict, source_key, dest_key, type, text=None):
    mapped_arrows_dict["type"] = type
    if text:
        mapped_arrows_dict["name"] = text
    mapped_arrows_dict["from"] = source_key
    mapped_arrows_dict["to"] = dest_key


class MapCreator:

    def __init__(self, mapped_code):
        self.mapped_code = mapped_code
        self.map_list = []
        self.current_mapped_classes = []
        self.current_mapped_methods = []

    def create_dictionary(self, task):
        full_task_dict = {"vertices": [], "edges": []}
        key = 0
        key, full_task_dict, query_key = self.create_query_task(task, full_task_dict, key)
        key, full_task_dict = self.create_class_component(task, full_task_dict, key, query_key)
        return self.task_dict(task, key, full_task_dict, flag=False)

    def task_dict(self, task, key, full_task_dict, **kwargs):
        if kwargs.get("flag"):
            flag = kwargs.get("flag")
        else:
            flag = False
        if not flag:
            for sub_class in task.sub_classes:
                key, full_task_dict = self.add_implemented_class(sub_class, full_task_dict, key)
        else:
            key, full_task_dict = self.add_implemented_class(task, full_task_dict, key)
        if not flag:
            for sub_class in task.sub_classes:
                key, full_task_dict = self.add_extended_class(sub_class, full_task_dict, key)
        else:
            key, full_task_dict = self.add_extended_class(task, full_task_dict, key)
        if not flag:
            for sub_class in task.sub_classes:
                if sub_class.class_name == "Workbook":
                    print("a")
                key, full_task_dict = self.create_method(sub_class, full_task_dict, key)
        else:
            key, full_task_dict = self.create_method(task, full_task_dict, key)
        if not flag:
            for sub_class in task.sub_classes:
                key, full_task_dict = self.add_calling_methods(sub_class, full_task_dict, key)
        else:
            key, full_task_dict = self.add_calling_methods(task, full_task_dict, key)
        if not flag:
            for sub_class in task.sub_classes:
                key, full_task_dict = self.add_sub_clases(sub_class, full_task_dict, key)
        else:
            key, full_task_dict = self.add_sub_clases(task, full_task_dict, key)
        return full_task_dict

    def add_sub_clases(self, code, full_task_dict, key):
        for sub_class in code.sub_classes:
            mapped_arrows_dict = {}
            mapped_task_dict = {}
            if sub_class.get_key() == 0:
                handle_vertex(mapped_task_dict, sub_class.class_name, key, comments=sub_class.documentation,
                              type="class", att_names=sub_class.get_class_atts_names())
                full_task_dict["vertices"].append(mapped_task_dict)
                sub_class.set_key(key)
                current_key = key
                key += 1
            else:
                current_key = sub_class.get_key()
            handle_edge(mapped_arrows_dict, code.get_key(), current_key, "method")
            full_task_dict["edges"].append(mapped_arrows_dict)
            self.task_dict(sub_class, key, full_task_dict, flag=True)
        return key, full_task_dict

    def create_query_task(self, code, full_task_dict, key):
        mapped_task_dict = {}
        code.set_key(key)
        query_key = key
        # handle_task(mapped_task_dict, code.query, key, comments=None, tags=code.tags,
        #             score=code.score, url=code.url, type="project", post=code.text)
        key += 1
        # full_task_dict["vertices"].append(mapped_task_dict)
        return key, full_task_dict, query_key

    def create_class_component(self, code, full_task_dict, key, query_key):
        for sub_class in code.sub_classes:
            mapped_task_dict = {}
            mapped_arrows_dict = {}
            sub_class.set_key(key)
            handle_vertex(mapped_task_dict, sub_class.class_name, key, comments=sub_class.documentation,
                          type="class", att_names=sub_class.get_class_atts_names())
            key += 1
            full_task_dict["vertices"].append(mapped_task_dict)
            handle_edge(mapped_arrows_dict, query_key, sub_class.get_key(), "class")
            full_task_dict["edges"].append(mapped_arrows_dict)
            self.current_mapped_classes.append(sub_class)
        return key, full_task_dict

    def add_implemented_class(self, code, full_task_dict, key):
        for implement_class in code.Implements:
            mapped_arrows_dict = {}
            handle_edge(mapped_arrows_dict, code.get_key(), implement_class.get_key(), "implements")
            full_task_dict["edges"].append(mapped_arrows_dict)
            key += 1
            self.current_mapped_classes.append(implement_class)
        return key, full_task_dict

    def add_extended_class(self, code, full_task_dict, key):
        if code.Extends is not None:
            mapped_arrows_dict = {}
            handle_edge(mapped_arrows_dict, code.get_key(), code.Extends.get_key(), "extends")
            full_task_dict["edges"].append(mapped_arrows_dict)
            key += 1
            self.current_mapped_classes.append(code.Extends)
        return key, full_task_dict

    def create_method(self, code, full_task_dict, key):
        for method in code.Methods:
            mapped_arrows_dict = {}
            mapped_task_dict = {}
            handle_vertex(mapped_task_dict, method.method_name, key, comments=method.documentation,
                          type="method", att_names=method.params)
            method.set_key(key)
            full_task_dict["vertices"].append(mapped_task_dict)
            handle_edge(mapped_arrows_dict, code.get_key(), key, "method")
            full_task_dict["edges"].append(mapped_arrows_dict)
            key += 1
            self.current_mapped_methods.append(method)
        return key, full_task_dict

    def create_attribute(self, code, full_task_dict, key):
        for sub_class in code.sub_classes:
            for attribute in sub_class.Attributes:
                mapped_arrows_dict = {}
                mapped_task_dict = {}
                handle_vertex(mapped_task_dict, attribute.name, key, type="attribute")
                attribute.set_key(key)
                full_task_dict["vertices"].append(mapped_task_dict)
                handle_edge(mapped_arrows_dict, sub_class.get_key(), key, "AchievedBy", "achieved by")
                full_task_dict["edges"].append(mapped_arrows_dict)
                key += 1
        return key, full_task_dict

    def get_method(self, method_name):
        for method in self.current_mapped_methods:
            if method.get_method_name() == method_name:
                return method
        return None

    def get_sub_class(self, class_name):
        for sub_class in self.current_mapped_classes:
            if sub_class.get_class_name() == class_name:
                return sub_class
        return None

    def add_calling_methods(self, code, full_task_dict, key):
        index_call = 1
        for method in code.Methods:
            for calling_method in method.calling_methods:
                mapped_arrows_dict = {}
                mapped_task_dict = {}
                linked_method = self.get_method(calling_method.method_name)
                if linked_method is None:
                    continue
                if linked_method.get_key() == 0:
                    handle_vertex(mapped_task_dict, method.method_name, key, type="method",
                                  att_names=method.params)
                    full_task_dict["vertices"].append(mapped_task_dict)
                    handle_edge(mapped_arrows_dict, method.get_key(), key, "method")
                    full_task_dict["edges"].append(mapped_arrows_dict, index_call=index_call)
                    index_call += 1
                    current_key = key
                    key += 1
                else:
                    current_key = linked_method.get_key()
                handle_edge(mapped_arrows_dict, method.get_key(), current_key, "method")
                full_task_dict["edges"].append(mapped_arrows_dict)
                index_call += 1
        return key, full_task_dict
