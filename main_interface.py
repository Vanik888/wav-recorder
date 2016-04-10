from configparser import ConfigParser
from tkinter import Tk, Button, Frame, Label, StringVar
from multiprocessing import Process, Queue
from time import sleep

import os

from common_libs.logger import CustomLogger
from recorder.recorder_cls import Recorder
from sender.sender import Sender
from analyzer.analyzer_cls import Analyzer

logger = CustomLogger().get_logger(module=__name__)

class GUI():
    def __init__(self):
        print('init called')
        self._init_speech_detector()
        self._root = Tk()
        self._root.after(100, func=self._update_result_label)
        self._control_panel = Frame(self._root, height=60, bg='gray')
        self._control_panel.pack(side='top', fill='x')
        self._working_frame = Frame(self._root, height=300, width=600)
        self._working_frame.pack(side='bottom', fill='both', expand=1)

        self._start_btn = Button(self._control_panel, text='Start')
        self._start_btn.bind("<Button-1>", self.start_ev)

        self._stop_btn = Button(self._control_panel, text='Stop')
        self._stop_btn.bind("<Button-1>", self.stop_ev)
        self._result_header = Label(self._working_frame, text='Result:')
        self._result_label = Label(self._working_frame, text='')

        # self._start_btn.pack(fill='both', side='top')
        # self._stop_btn.pack(fill='both', side='top')
        self._start_btn.place(x=10, y=10, width=40, height=40)
        self._stop_btn.place(x=60, y=10, width=40, height=40)
        self._result_header.place(x=10, y=10, width=40, height=40)
        self._result_label.place(x=60, y=10, width=200, height=40)

        self._result_queue = Queue()


    def _init_speech_detector(self):
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

    def stop_ev(self, ev):
        print("stop is clicked")
        print("Is alive %s" % self.analyze_proc.is_alive())
        self.analyze_proc.terminate()
        sleep(1)
        print("Is alive %s" % self.analyze_proc.is_alive())

    def start_ev(self, ev):
        print("start is clicked")
        self.analyze_proc = Process(name="Analyze Process", group=None, target=self.analyze_work, args=(self._result_queue,))
        self.analyze_proc.start()
        # self.proc.join()

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

    def _update_result_label(self):
        if not self._result_queue.empty():
            self._result_label.config(text=self._result_queue.get(), width=200)
        self._root.after(100, func=self._update_result_label)


    def start_gui(self):
        self._root.mainloop()


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

    def main(self):
        while True:
            self.record_to_file()
            self.send()
            result = self.analyze()
            logger.info(result)
            if result is not None:
                print('Распознанный код команды %s навание команды %s' % result)

if __name__ == '__main__':
    # main_program = MainInterface()
    # main_program.main()
    gui = GUI()
    gui.start_gui()


