from configparser import ConfigParser

import os

from common_libs.logger import CustomLogger
from recorder.recorder_cls import Recorder
from sender.sender import Sender
from analyzer.analyzer_cls import Analyzer

logger = CustomLogger().get_logger(module=__name__)


class MainInterface():
    def __init__(self):
        self._config_parser = ConfigParser()
        self._read_config()
        self._sender = Sender(**self._get_section_dict('sender'))
        self._recorder = Recorder(**self._get_section_dict('recorder'))
        result_file = os.path.join(os.getcwd(), 'stat', 'xmls', 'result.xml')
        self._analyzer = Analyzer(result_file)

    def _read_config(self):
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_FILE = os.path.join(CURRENT_DIR, 'global.cfg')
        self._config_parser.read(CONFIG_FILE)

    def _get_section_dict(self, section):
        dict = {}
        for item in self._config_parser.items(section):
            dict[item[0].upper()] = item[1]
        return dict

    def record_to_file(self):
        self._recorder.record_to_file()

    def send(self):
        self._sender.send()

    def analyze(self):
        return self._analyzer.analyze()

if __name__ == '__main__':
    main_program = MainInterface()
    while True:
        main_program.record_to_file()
        main_program.send()
        result = main_program.analyze()
        logger.info(result)
        if result is not None:
            print('Распознанный код команды %s навание команды %s' % result)


