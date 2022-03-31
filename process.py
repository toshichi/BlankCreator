import re
import copy
import operator
import os

import argparse

class Helper:

    # check if (2,3) is in [(0,1), (3,5)] (True)
    # or if (2,3) is in [(0,1), (4,5)] (False)
    @staticmethod
    def is_in_range(num: tuple, ranges: list) -> bool:
        for _range in ranges:
            for _i in num:
                if _range[0] <= _i <= _range[1]:
                    return True
            for _i in _range:
                if num[0] <= _i <= num[1]:
                    return True
        return False

    @staticmethod
    def get_files(input_dir):
        files_list = []
        for _fpath, _, _files in os.walk(input_dir):
            # for all txt files in folder
            for _file in _files:
                if _file.split(".")[-1].lower() in ["txt"]:
                    files_list.append(
                        os.path.join(_fpath, _file))
        return files_list



class BlankCreator:
    
    # In a certain range, pattern in the front has higher priority
    # %function_name : function name of the recursion function
    regex_patterns_raw = {
        "target_function": {
            # self regex:[regex, function_name_group, function_content_group]
            "self": [r"^(int|float|double|long|void|char\*)\s((?!main).+)\s?\(.+\)\s?\n?\{((.|\s)*?)^\}", 2, 3],
            "blanks": [
                # blank regex: [regex, blank_group, make blank/except blank(True/False)]
                [r"^(.+?)(\[noblankbefore\])", 1, False],
                [r"(\[noblankbetween\])(.+?)(\[\/noblankbetween\])", 2, False],
                [r"^(.+?)(\[blankbefore\])", 1, True],
                [r"(\[blankbetween\])(.+?)(\[\/blankbetween\])", 2, True],
                [r"%function_name\s?\((.+)\);", 1, True],
                [r"(if|while)\s?\((.+)\)", 2, True],
                [r"(printf|scanf)\s?\((.+)\)", 2, True],
                [r"return\s(.+?);", 1, True]
                # [r"return\s((?!%function_name).+);", 1]
            ]
        },
        "main_function": {
            "self": [r"^(int|void)\s(main)\s?\(.*\)\s?\n?\{((.|\s)*?)^\}", 2, 3],
            "blanks": [
                [r"^(.+?)(\[noblankbefore\])", 1, False],
                [r"(\[noblankbetween\])(.+?)(\[\/noblankbetween\])", 2, False],
                [r"^(.+?)(\[blankbefore\])", 1, True],
                [r"(\[blankbetween\])(.+?)(\[\/blankbetween\])", 2, True],
                [r"%function_name\s?\((.+)\);", 1, True],
                [r"(if|while)\s?\((.+)\)", 2, True],
                [r"(printf|scanf)\s?\((.+)\)", 2, True],
                [r"return\s([^0]+?);", 1, True],
                [r"^(\s*)(\S+)\s?\=\s?.*\((((signed|unsigned|short|long|char|float|double|wchar_t|bool|int)\s){0,3}(signed|unsigned|short|long|char|float|double|wchar_t|bool|int))\)(\S+);", 3, True]
            ]
        }    
    }

    mark_strings = [
        "[blankbefore]",
        "[noblankbefore]",
        "[blankbetween]",
        "[/blankbetween]",
        "[noblankbetween]",
        "[/noblankbetween]"
    ]


    def __init__(self, text):
        self.text = text
        self.get_target_function()
        self.pattern_process()
        

    def get_target_function(self):
        _regex = self.regex_patterns_raw["target_function"]["self"]
        matched = re.search(_regex[0], self.text, re.MULTILINE)
        if matched == None:
            # only main function
            self.target_function_name = "-=impossible-function-name=-"
            # self.target_function_content = ""
        else:
            self.target_function_name = matched.group(_regex[1])
            # self.target_function_content = matched.group(_regex[2])

    def pattern_process(self):
        # pattern process
        self.regex_patterns = copy.deepcopy(self.regex_patterns_raw)
        for part_key in self.regex_patterns:
            for pattern in self.regex_patterns[part_key]["blanks"]:
                pattern[0] = pattern[0].replace(r"%function_name", self.target_function_name)

    def bracket_verify(self, span: tuple):
        _count = 0
        for i,c in enumerate(self.text[span[0]:span[1]]):
            if c == '(':
                _count += 1
            elif c == ')':
                _count -= 1
                if _count < 0:
                    return (span[0], span[0] + i)
        return span
            

    def determine_blank_position(self):
        matched_blanks = []
        excepted_blanks = []
        for part_key in self.regex_patterns:
            _regex_self = self.regex_patterns[part_key]["self"]
            for part_content in re.finditer(_regex_self[0], self.text, re.MULTILINE):
                part_offset = part_content.span(_regex_self[2])[0]
                part_text = part_content.group(_regex_self[2])
                for _regex_blank in self.regex_patterns[part_key]["blanks"]:
                    for blank in re.finditer(_regex_blank[0], part_text, re.MULTILINE):
                        span_relative = blank.span(_regex_blank[1])
                        # add offset to span
                        span = tuple(map(operator.add, span_relative, (part_offset, part_offset)))
                        # if regex contains bracket, verify pairing
                        if r"\(" in _regex_blank[0]:
                            span = self.bracket_verify(span)
                        if not Helper.is_in_range(span, matched_blanks + excepted_blanks):
                            # check this rule is to make blank or to skip blank
                            if _regex_blank[2]: # make
                                matched_blanks.append(span)
                            else:
                                excepted_blanks.append(span)
        
        return sorted(matched_blanks, key=lambda x: x[0])

    def make_blanks(self):
        blanks = self.determine_blank_position()
        self.text_question = ""
        self.text_answer = []
        _last_end = 0
        blank_num = 1
        for blank in blanks:
            self.text_question += self.text[_last_end:blank[0]]
            self.text_answer.append(self.text[blank[0]:blank[1]])
            self.text_question += " _%d_ " % blank_num
            blank_num += 1
            _last_end = blank[1]
        self.text_question += self.text[_last_end:]
        # remove marks
        for mark in self.mark_strings:
            self.text_question = self.text_question.replace(mark, "")

def main(dir_path):
    files = Helper.get_files(dir_path)
    output_dir = os.path.join(dir_path, "..", "output")
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    for file in files:
        with open(file, 'r') as f_input:
            text = f_input.read()
        maker = BlankCreator(text)
        maker.make_blanks()
        print("Processed %s, %d blanks created" % (file, len(maker.text_answer)))
        _output_text = maker.text_question + '\n\n' + ',,'.join(maker.text_answer).replace(" ","").replace("\t", "") + ',,'

        _filename = os.path.basename(file)
        with open(os.path.join(output_dir, _filename), 'w') as f_output:
            f_output.write(_output_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creating blanks for C language source code files")
    parser.add_argument('source_dir', type=str, help="The directory containing source code files to be processed.")
    args = parser.parse_args()
    main(args.source_dir)