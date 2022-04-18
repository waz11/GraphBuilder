from os.path import dirname
import re
import pandas as pd
import javalang
from collections import namedtuple
from itertools import takewhile
from enum import Enum
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

class Errors(Enum):
    FAILED_PARSING = 1
    PYTHON_EXCEPTION = 2


Position = namedtuple('Position', ['line', 'column'])
PATH = dirname(__file__)
temp_dir = dirname(dirname(__file__))

Body_Dict = namedtuple('Body_Dict', ['text', 'code', 'tags', 'post_id'])
Post_Dict = namedtuple('post_dict', ['text', 'code', 'score'])

primitive_types = ['Boolean', 'boolean', 'char', 'byte', 'short', 'int', 'long', 'float', 'double', 'String', 'string',
                   'System', 'System.out', 'Scanner', 'Log']


class codeExtractor:

    def __init__(self, dataset=None, path=None):
        if path is None:
            self.body_df = dataset[["title", "body", "tags", "post_id"]]
            self.answer_df = dataset[["title", "answers_body", "score"]]
            self.body_df = self.body_df.drop_duplicates(subset=['title'])
            self.body_mapping = {}
            self.answer_mapping = {}
        else:
            self.data = pd.read_csv(path)
        self.words = []
        self.all_text = []

    def extractCodes(self):
        tags = ""
        for index, df_row in self.body_df.iterrows():
            text, code = self.extract_code_text_to_dict(df_row['body'])

            if pd.notna(df_row['tags']):
                tags = df_row['tags'].split('|')  # extract the tags
            post_id = df_row["post_id"]

            body_dict = Body_Dict(text, code, tags, post_id )  # adds everything to the new dict
            self.body_mapping[df_row['title']] = body_dict
            self.answer_mapping[df_row['title']] = []  # prepare the title to the answer

        """handle the answers"""
        for index, df_row in self.answer_df.iterrows():
            try:
                text, code = self.extract_code_text_to_dict(df_row['answers_body'])
            except TypeError:
                continue
            body_dict = Post_Dict(text, code, df_row['score'])  # adds the comment score
            self.answer_mapping[df_row['title']].append(body_dict)

        return self.body_mapping, self.answer_mapping

    def extract_code_text_to_dict(self, post):
        """
        extract_code_text_to_dict Function - extract the code and the text from each post
        :param post:
        :return text, code after the data preprocess
        """
        text = ""
        code = []
        for curr_text in re.findall(r"<p>(.*?)</p>", post, flags=re.DOTALL):  # extract the text
            text += curr_text
            text = re.sub("<code>(.*?)</code>", '', text)
            text = text.replace('&gt;', '>')
            text = text.replace('&lt;', '<')
            text = text.replace('&amp;&amp;', '&&')
            text = text.replace('&amp;', '&')
            text = text.replace('&quot;', '"')
            # word_tokens = word_tokenize(text)

            # self.words += [w for w in word_tokens if not w in stop_words]
            self.all_text.append(text)
        row = re.sub('<p>.*?</p>', '', post)  # remove the text

        for curr_code in re.findall(r"<code>(.*?)</code>", row, flags=re.DOTALL):  # extract the code
            """handle html tags from crawler"""
            curr_code = curr_code.replace('&gt;', '>')
            curr_code = curr_code.replace('&lt;', '<')
            curr_code = curr_code.replace('&amp;&amp;', '&&')
            curr_code = curr_code.replace('&amp;', '&')
            curr_code = curr_code.replace('&quot;', '"')
            curr_code = curr_code.replace('[...]', '')  # TODO: TEST IF WORKING
            curr_code = curr_code.replace('...', '/** ...*/')

            code.append(curr_code)

        for index in range(len(code)):
            search_comments = re.findall("//(.*?)\n", code[index], flags=re.DOTALL)
            for comment in search_comments:
                if "/**" not in comment:
                    code[index] = code[index].replace("//" + comment, '/**' + comment + "*/")

        return text, code

def extract_specific_code(position, parser_token_list, obj, current_query, modifiers=None):
    current_query.changed_code()  # notify that code has been changed
    start_index = 0
    for token in parser_token_list:
        if token.position == position:
            break
        start_index += 1
    if modifiers is not None:
        while start_index > 0 and position[0] == parser_token_list[start_index].position[0]:
            start_index -= 1
        if start_index != 0:
            start_index += 1
        col_position = parser_token_list[start_index].position[1]
    else:
        col_position = position[1]
    end_index = start_index + 1
    for index in range(start_index + 1, len(parser_token_list)):
        if parser_token_list[index].position[1] == col_position and parser_token_list[index].value == '}':
            if isinstance(parser_token_list[index], javalang.tokenizer.Separator):
                break
        end_index += 1
    code = javalang.tokenizer.reformat_tokens(parser_token_list[start_index:end_index + 1])  # get the code
    return code


def create_collected_code(query):
    new_code = ""
    non_changed_classes = []
    if query.imports_codes is not []:
        for _import in query.imports_codes:
            new_code += "import " + _import + ';\n'
    for sub_class in query.sub_classes:
        if not sub_class.code_changed:
            if sub_class.code is not None:
                new_code += sub_class.code
        else:
            non_changed_classes.append(sub_class)
    for modified_class in non_changed_classes:
        if modified_class.code is None:
            continue
        new_class_code = ""
        new_class_code += modified_class.code.split('{')[0] + "{\n"
        whitespace = list(takewhile(str.isspace, new_class_code))
        "".join(whitespace)
        indent = len(whitespace) + 4
        for class_enum in modified_class.Enums:
            new_class_code += (' ' * indent) + class_enum.code
        for class_attributes in modified_class.Attributes:
            if class_attributes.code not in new_class_code:
                new_class_code += (' ' * indent) + class_attributes.code
        for class_method in modified_class.Methods:
            if class_method.code is not None:
                new_indent = '\n ' + ' ' * indent
                method_code = class_method.code.replace('\n', new_indent)
                new_class_code += (' ' * indent) + method_code + '\n '
        new_class_code += (' ' * (indent - 4)) + '}' + '\n'

        modified_class.code = new_class_code
        new_code += modified_class.code
    query.code = new_code


def extract_att_code(position, parser_token_list, current_query, modifiers=None):
    current_query.changed_code()
    start_index = 0
    for token in parser_token_list:
        if token.position == position:
            break
        start_index += 1
    if modifiers is not None:
        while start_index > 0 and position[0] == parser_token_list[start_index].position[0]:
            start_index -= 1
        start_index += 1
    end_index = start_index + 1
    for index in range(start_index + 1, len(parser_token_list)):
        if parser_token_list[index].position[0] != position[0]:
            break
        end_index += 1
    code = javalang.tokenizer.reformat_tokens(parser_token_list[start_index:end_index])  # get the code
    return code