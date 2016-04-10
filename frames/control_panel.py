# -*- coding: utf-8 -*-

from multiprocessing import Process
from time import sleep

from tkinter import Frame, Button

class ControlPanel():
    def __init__(self, *args, **kwargs):
        self._root = kwargs['root']
        self._result_queue = kwargs['result_queue']
        self._sender = kwargs['sender']
        self._recorder = kwargs['recorder']
        self._analyzer = kwargs['analyzer']

        self.frame = Frame(self._root, height=60, bg='gray')
        self.frame.pack(side='top', fill='x')

        self.start_btn = Button(self.frame, text='Start')
        self.start_btn.bind('<Button-1>', self.start_ev)

        self.stop_btn = Button(self.frame, text='Stop')
        self.stop_btn.bind('<Button-1>', self.stop_ev)
        self.place_content()


    def place_content(self):
        self.start_btn.place(x=10, y=10, width=40, height=40)
        self.stop_btn.place(x=60, y=10, width=40, height=40)

    # запускаем процесс анализа
    def start_ev(self, ev):
        print("start is clicked")
        self.analyze_proc = Process(name="Analyze Process", group=None, target=self.analyze_work, args=(self._result_queue,))
        self.analyze_proc.start()
        # self.proc.join()

    # киляем проецесс анализа
    def stop_ev(self, ev):
        print("stop is clicked")
        print("Is alive %s" % self.analyze_proc.is_alive())
        self.analyze_proc.terminate()
        sleep(1)
        print("Is alive %s" % self.analyze_proc.is_alive())

    # записываем слово в файл
    def record_to_file(self):
        self._recorder.record_to_file()

    # отправляем запись на сервер
    def send(self):
        self._sender.send()

    # анализируем ответ сервера
    def analyze(self):
        return self._analyzer.analyze()


    # полный цикл: запись - отправка на сервер- анализ
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
