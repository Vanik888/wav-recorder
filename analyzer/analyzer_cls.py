import os

from analyzer.libs.xml_parser import XmlParser
from common_libs.logger import CustomLogger

logger = CustomLogger().get_logger(module=__name__)


class Analyzer:
    def __init__(self, xml_abs_path):
        self._xml_parser = XmlParser(xml_abs_path)

    def analyze(self):
        self._result_list = self._xml_parser.get_result_list()
        self.sort_result_list()
        logger.info([item for item in self._result_list])

        for item in self._result_list:
            dictionary_id = self._search_word_in_dict(item.get_value())
            if dictionary_id is not None:
                return dictionary_id, item.get_value()
        print("Команду не удалось распознать")

    def sort_result_list(self):
        self._result_list.sort(key=lambda x: x.get_confidence(), reverse=True)

    def _search_word_in_dict(self, word):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dict_dir = os.path.join(script_dir, 'commands_dictionary', 'dictionary')
        f = open(dict_dir, 'rt')
        for line in f:
            code, description = line.split('=')
            code = int(code.strip())
            description = description.strip()
            logger.info("compare"
                         ": %s ? %s" % (word.upper(), description.upper()))
            # TODO-vanik: remove next line
            # print("%s ? %s" % (word.upper(), description.upper()))
            if word.upper() == description.upper():
                return code
        return None

if __name__ == '__main__':
    print(os.getcwd())
    result_file = os.path.join(os.getcwd(), 'stat', 'xmls', 'result.xml')
    analyzer = Analyzer(result_file)
    result = analyzer.analyze()
    print(result)
    if result is not None:
        print('Распознанный код команды %s навание команды "%s"' % result)

