import os

from analyzer.libs.xml_parser import XmlParser
from common_libs.logger import CustomLogger
from analyzer.commands_dictionary.menu import menu

logger = CustomLogger().get_logger(module=__name__)


class Analyzer:
    def __init__(self, xml_abs_path):
        self._xml_parser = XmlParser(xml_abs_path)

    def analyze(self, where_to_search):
        self._result_list = self._xml_parser.get_result_list()
        self.sort_result_list()
        logger.info([item for item in self._result_list])


        stored_data = menu[where_to_search]
        for item in self._result_list:
            for k, v in stored_data.items():
                if v['name'].upper() == item.get_value().upper():
                    return k
        print("Команду не удалось распознать")
        return None

    def sort_result_list(self):
        self._result_list.sort(key=lambda x: x.get_confidence(), reverse=True)

if __name__ == '__main__':
    print(os.getcwd())
    result_file = os.path.join(os.getcwd(), 'stat', 'xmls', 'result.xml')
    analyzer = Analyzer(result_file)
    result = analyzer.analyze()
    print(result)
    if result is not None:
        print('Распознанный код команды %s навание команды "%s"' % result)

