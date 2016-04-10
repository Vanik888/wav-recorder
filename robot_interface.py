from configparser import ConfigParser
from tkinter import Tk, Button, Frame, Label, StringVar
from multiprocessing import Process, Queue
from time import sleep

import os

from common_libs.logger import CustomLogger
from recorder.recorder_cls import Recorder
from sender.sender import Sender
from analyzer.analyzer_cls import Analyzer
from frames.control_panel import ControlPanel

logger = CustomLogger().get_logger(module=__name__)

class GUI():
    def __init__(self):
        print('init called')
        self._result_queue = Queue()

        self._init_speech_detector()
        self._root = Tk()
        self._root.after(100, func=self._update_result_label)

        self._control_panel = ControlPanel(root=self._root,
                                           result_queue=self._result_queue,
                                           sender=self._sender,
                                           recorder=self._recorder,
                                           analyzer=self._analyzer)
        self._control_panel.frame.pack(side='top', fill='x')

        self._working_frame = Frame(self._root, height=300, width=600)
        self._working_frame.pack(side='bottom', fill='both', expand=1)

        self._result_header = Label(self._working_frame, text='Result:')
        self._result_label = Label(self._working_frame, text='')

        self._result_header.place(x=10, y=10, width=40, height=40)
        self._result_label.place(x=60, y=10, width=200, height=40)



    # инициализируем систему анализа речи
    def _init_speech_detector(self):
        self._config_parser = ConfigParser()
        self._read_config()
        self._sender = Sender(**self._get_section_dict('sender'))
        self._recorder = Recorder(**self._get_section_dict('recorder'))
        result_file = os.path.join(os.getcwd(), 'stat', 'xmls', 'result.xml')
        self._analyzer = Analyzer(result_file)

    # читаем конфиг из файла
    def _read_config(self):
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_FILE = os.path.join(CURRENT_DIR, 'global.cfg')
        self._config_parser.read(CONFIG_FILE)

    # возвращаем словарь полей из конфига
    def _get_section_dict(self, section):
        dict = {}
        for item in self._config_parser.items(section):
            dict[item[0].upper()] = item[1]
        return dict

    # дергаем очередь на наличие ответа
    def _update_result_label(self):
        if not self._result_queue.empty():
            self._result_label.config(text=self._result_queue.get(), width=200)
        self._root.after(100, func=self._update_result_label)


    def start_gui(self):
        self._root.mainloop()



if __name__ == '__main__':
    gui = GUI()
    gui.start_gui()


