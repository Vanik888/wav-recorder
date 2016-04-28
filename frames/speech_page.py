# -*- coding: utf-8 -*-

from tkinter import Frame, Label, PhotoImage, Button
from multiprocessing import Process, Queue
from time import sleep

from frames.analyze_frame_mixin import AnalyzeFrameMixin
from frames.comon_frame_mixin import CommonFrameMixin
from analyzer.commands_dictionary.menu import menu_pages

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
        self.icon_lbl = Label(self, text='Говорите', justify='center', image=self.icon_lbl_img, font=("Helvetica", 26, "bold"), compound='right')

        self.status_lbl = Label(self, text='Запись речи', justify='center', font=("Helvetica", 16, "bold"))

        btns_txt_len = 20
        self.return_btn_img = PhotoImage(file='./stat/inteface_images/back.png')
        self.return_btn = Button(self, text=self.add_spaces_to_str(btns_txt_len, 'Назад'), image=self.return_btn_img, compound='right', height=100, width=300)
        self.return_btn.bind('<Button-1>', self.return_ev)

        # задача на апдейт страницы
        self._job = None
        self.back_page = None
        # self.back_page_child_frame = None
        self.place_content()


    def place_content(self):
        icon_lbl_size = {'height': 180, "width": 400}
        status_lbl_size = {'height': 180, "width": 400}
        return_btn_size = {'height': 180, "width": 400}

        self.icon_lbl.place(x=220, y=10, **icon_lbl_size)
        # self.icon_lbl.pack( fill='x')
        self.status_lbl.place(x=200, y=200, **status_lbl_size)
        # self.status_lbl.pack(fill='both')
        self.return_btn.place(x=200, y=400, **return_btn_size)
        # self.return_btn.pack(fill='x')

    def return_ev(self, ev):
        print('clicked return_btn')
        print("Is alive %s" % self.analyze_proc.is_alive())
        self.analyze_proc.terminate()
        sleep(1)
        print("Is alive %s" % self.analyze_proc.is_alive())
        self.move_to_page()


    def _update_result_label(self):
        print('update_result_label called')

        if not self._result_queue.empty():
            txt, page_to_move = self._result_queue.get()
            self.status_lbl.config(text=txt, width=200)
            if page_to_move is not None:
                self.move_to_page(page_to_move)
        self._job = self.after(100, func=self._update_result_label)


    # метод вызывается из окна с меню при тыке на кнопку говорите
    def start_request_proc(self):
        # привязываем апдейтилку
        # начинаем запрос
        self._job = self.after(100, func=self._update_result_label)
        self.analyze_proc = Process(name="Analyze Process", group=None, target=self.analyze_work, args=(self._result_queue, menu_pages[self.back_page]))
        self.analyze_proc.start()

    def analyze_work(self, result_queue, where_to_search):
        print('analyze work started')
        result_queue.put(('1', None))
        sleep(0.5)
        result_queue.put(('2', None))
        sleep(0.5)
        result_queue.put(('3', None))
        sleep(0.5)
        result_queue.put(('Начинаем запись', None))
        print('started analyzer proc')
        # self.record_to_file()
        result_queue.put(("Запрос записан", None))
        sleep(0.5)
        result_queue.put(("Отправка", None))
        # self.send_file()
        sleep(0.5)
        result_queue.put(("Проверка", None))
        result = self.analyze(where_to_search)
        sleep(0.5)
        if result is not None:
            print('result found: %s' % str(result))
            result_queue.put(("Переход", result))
        else:
            result_queue.put(('Ничего не нашлось', None))

    def move_to_page(self, found_page=None):
        print('show page %s' % str(self.back_page))
        self._controller.show_frame(self.back_page)
        if found_page:
            self._controller.current_frame.show_frame(found_page)
        self.destroy()





