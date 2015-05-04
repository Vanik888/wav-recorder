import os

from libs.xml_parser import XmlParser


class Analyzer:
    def __init__(self, xml_abs_path):
        self._xml_parser = XmlParser(xml_abs_path)
        self._result_list = self._xml_parser.get_result_list()

    def analyze(self):
        for i in self._result_list:
            print(i.get_confidence(), i.get_value())

    def _search_word_in_dict(self, word):
        f = open('./commands_dictionary/dictionary', 'rt')
        for line in f:
            code, description = line.split('=')
            code = int(code.strip())
            description = description.strip()
            if word == description:
                return code
        return None



if __name__ == '__main__':
    print(os.getcwd())
    analyzer = Analyzer('../sender/output/result.xml')
    analyzer.analyze()
    code = analyzer._search_word_in_dict('назад')
    if code is not None:
        print(code)

