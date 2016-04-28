# -*- coding: utf-8 -*-

from configparser import ConfigParser
from time import sleep

import os

from sender.sender import Sender
from recorder.recorder_cls import Recorder
from analyzer.analyzer_cls import Analyzer

# Миксин включающий все необходимые методы для анализа речи
class AnalyzeFrameMixin():
    def __init__(self):
        self._config_parser = None
        self._sender = None
        self._analyzer = None
        self._recorder = None

    def _init_speech_detector(self):
        self._config_parser = ConfigParser()
        self._read_config()
        self._sender = Sender(**self._get_section_dict('sender'))
        self._recorder = Recorder(**self._get_section_dict('recorder'))
        result_file = os.path.join(os.getcwd(), 'stat', 'xmls', 'result.xml')
        self._analyzer = Analyzer(result_file)

    def _read_config(self):
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        print(CURRENT_DIR)
        print(os.getcwd())
        CURRENT_DIR = os.getcwd()
        CONFIG_FILE = os.path.join(CURRENT_DIR, 'global.cfg')
        self._config_parser.read(CONFIG_FILE)

    def _get_section_dict(self, section):
        dict = {}
        for item in self._config_parser.items(section):
            dict[item[0].upper()] = item[1]
        return dict

    def record_to_file(self):
        self._recorder.record_to_file()

    def send_file(self):
        self._sender.send()

    def analyze(self, where_to_search):
        return self._analyzer.analyze(where_to_search)

    def analyze_work(self, result_queue):
        print('started analyzer proc')
        # self.record_to_file()
        result_queue.put("data recorded")
        sleep(0.5)
        # self.send()
        result_queue.put("data sended")
        sleep(0.5)
        # result = self.analyze()
        result_queue.put("get the answer")
        sleep(1)

