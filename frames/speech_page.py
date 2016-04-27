# -*- coding: utf-8 -*-

from tkinter import Frame, Label, PhotoImage, Button
from multiprocessing import Process, Queue

from frames.analyze_frame_mixin import AnalyzeFrameMixin
from frames.comon_frame_mixin import CommonFrameMixin

class SpeechPage(Frame, CommonFrameMixin, AnalyzeFrameMixin):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, kwargs['root'], **kwargs['frame_size'])
        self._root = kwargs['root']
        self._controller = kwargs['controller']
        self._frame_size = kwargs['frame_size']

        # очередь с данными на сервере
        self._result_queue = Queue()
        self._init_speech_detector()

        self.icon_lbl_img = PhotoImage(file='./stat/inteface_images/speak.png')
        self.icon_lbl = Label(self, text='Говорите', anchor='n', image=self.icon_lbl_img, font=("Helvetica", 26, "bold"), compound='right')
        self.status_lbl = Label(self, text='Запись речи', anchor='n', font=("Helvetica", 16, "bold"))


        btns_txt_len = 20
        self.return_btn_img = PhotoImage(file='./stat/inteface_images/back.png')
        self.return_btn = Button(self, text=self.add_spaces_to_str(btns_txt_len, 'Назад'), image=self.return_btn_img, compound='right')
        self.return_btn.bind('<Button-1>', self.return_ev)

        self.place_content()


    def place_content(self):
        self.icon_lbl.pack(fill='x', expand=1)
        self.status_lbl.pack(fill='both', expand=1)
        self.return_btn.pack(fill='both', expand=1)

    def return_ev(self, ev):
        print('clicked return_btn')
        self._controller.show_frame('DishPage')


