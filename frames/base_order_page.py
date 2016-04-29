# -*- coding: utf-8 -*-


from tkinter import Frame, Button, Label, PhotoImage

from frames.dish_image_frame import DishImageFrame
from frames.comon_frame_mixin import CommonFrameMixin
from analyzer.commands_dictionary.menu import menu
from menu.base_order_item import BaseOrderItem



class BaseOrderPage(Frame, CommonFrameMixin):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, kwargs['root'], **kwargs['frame_size'])

        self._root = kwargs['root']
        self._controller = kwargs['controller']
        self._frame_size = kwargs['frame_size']

        header_txt = kwargs['header_txt']
        # используется для формирования сета из подменюшек
        self.order_type = kwargs['order_type']

        self.header = Label(self, text=header_txt, anchor='se', font=("Helvetica", 16, "bold"))

        # Длина сторки с текстом на кнопке
        btns_txt_len = 20
        self.btn_font = self.get_bnt_font()
        self.speech_btn_img = PhotoImage(file='./stat/inteface_images/speak.png')
        self.speech_btn = Button(self, text=self.add_spaces_to_str(btns_txt_len, 'Говорите'), image=self.speech_btn_img, compound='right', font=self.btn_font)
        self.speech_btn.bind('<Button-1>', self.speech_ev)

        self.return_btn_img = PhotoImage(file='./stat/inteface_images/back.png')
        self.return_btn = Button(self, text=self.add_spaces_to_str(btns_txt_len, 'Назад'), image=self.return_btn_img, compound='right', font=self.btn_font)
        self.return_btn.bind('<Button-1>', self.return_ev)

        self.add_btn_img = PhotoImage(file='./stat/inteface_images/add.png')
        self.add_btn = Button(self, text=self.add_spaces_to_str(btns_txt_len, 'Добавить'), image=self.add_btn_img, compound='right', font=self.btn_font)
        self.add_btn.bind('<Button-1>', self.add_ev)

        self.remove_btn_img = PhotoImage(file='./stat/inteface_images/remove.png')
        self.remove_btn = Button(self, text=self.add_spaces_to_str(btns_txt_len, 'Убрать'), image=self.remove_btn_img, compound='right', font=self.btn_font)
        self.remove_btn.bind('<Button-1>', self.remove_ev)


        self.next_btn_img = PhotoImage(file='./stat/inteface_images/right.png')
        self.next_btn = Button(self, image=self.next_btn_img)
        self.next_btn.bind('<Button-1>', self.next_ev)

        self.previous_btn_img = PhotoImage(file='./stat/inteface_images/left.png')
        self.previous_btn = Button(self, image=self.previous_btn_img)
        self.previous_btn.bind('<Button-1>', self.previous_ev)

        # поле с картинкой
        self.container = Frame(self)
        self._container_size = {'height': 400, 'width': 600}
        self.child_frame = None

        self.frames = {}
        self.frames_set = self.create_orders_set()

        for i,f in enumerate(self.frames_set):
            page_name = f.__name__
            frame = DishImageFrame(root=self.container, controller=self, frame_size=self._container_size, dish=f)

            # проставляем названия следующиего и предыдущего блюда
            if i == 0:
                frame.next = self.frames_set[i+1].__name__
                frame.previous = self.frames_set[len(self.frames_set)-1].__name__
            elif i == len(self.frames_set)-1:
                frame.next = self.frames_set[0].__name__
                frame.previous = self.frames_set[i-1].__name__
            else:
                frame.next = self.frames_set[i+1].__name__
                frame.previous = self.frames_set[i-1].__name__


            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            # frame.pack(side='top', fill='x')
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame((self.frames_set[0]).__name__)

        self.place_content()


    def place_content(self):
        click_btn_size = {'height': 70, 'width': 360}
        move_btn_size = {'height': 100, 'width': 100}
        header_size = {'height': 40, 'width': 200}

        header_y_pad = 3

        # разница по высоте= общая высота - 2 кнопки - форма с описанием
        y_diff = (self._frame_size['height'] - click_btn_size['height']*2 - self._container_size['height'] - header_size['height']-header_y_pad*2)/4
        x_diff = (self._frame_size['width']-click_btn_size['width']*2)/3
        click_btn_col2 = click_btn_size['width']+ 2*x_diff
        # начальная координата хидера: по середине
        header_x_pos = self._frame_size['width']/2 - header_size['width']/2 + 20

        self.header.place(x=header_x_pos, y=header_y_pad)
        self.speech_btn.place(x=x_diff, y=(header_size['height']+header_y_pad*2), **click_btn_size)
        self.return_btn.place(x=click_btn_col2, y=(header_size['height']+header_y_pad*2), **click_btn_size)

        self.add_btn.place(x=x_diff, y=(header_size['height'] + header_y_pad*2 + click_btn_size['height']+self._container_size['height']+y_diff*3), **click_btn_size)
        self.remove_btn.place(x=click_btn_col2, y=(header_size['height'] + header_y_pad*2 + click_btn_size['height']+self._container_size['height']+y_diff*3), **click_btn_size)

        print('y1 header=%s' % header_y_pad )
        print('y2 click btns=%s' % (header_size['height']+ header_y_pad*2 + y_diff))
        print('y3 containter=%s' % (header_size['height']+ header_y_pad*2 + click_btn_size['height'] + y_diff*2))
        print('y4 click btns_down=%s' % (header_size['height']+header_y_pad*2 + click_btn_size['height'] + self._container_size['height'] + y_diff*3))

        x_diff = (self._frame_size['width'] - self._container_size['width'] - move_btn_size['width']*2) / 4

        self.container.place(x=x_diff*2+move_btn_size['width'], y=(header_size['height']+ header_y_pad*2 + click_btn_size['height'] + y_diff*2))
        self.previous_btn.place(x=x_diff, y=(header_size['height']+ header_y_pad*2 + click_btn_size['height'] + y_diff*2 + self._container_size['height']/2 - move_btn_size['height']/2), **move_btn_size)
        self.next_btn.place(x=x_diff*3 + move_btn_size['width'] + self._container_size['width'] , y=(header_size['height']+ header_y_pad*2 + click_btn_size['height'] + y_diff*2 + self._container_size['height']/2 - move_btn_size['height']/2), **move_btn_size)


    def speech_ev(self, ev):
        print('clicked speech_btn')
        back_page = type(self).__name__
        self._controller.show_frame('SpeechPage')
        self._controller.current_frame.back_page = back_page

        print("pass to speach frame %s"  % back_page)

        self._controller.current_frame.start_request_proc()

    def return_ev(self, ev):
        print('clicked return_btn')
        self._controller.show_frame('StartPage')

    def add_ev(self, ev):
        self.child_frame.add_dish()
        print('clicked add_btn')

    def remove_ev(self, ev):
        self.child_frame.remove_dish()
        print('clicked remove_btn')

    def next_ev(self, ev):
        self.show_frame(self.child_frame.next)
        print('clicked next_btn')

    def previous_ev(self, ev):
        self.show_frame(self.child_frame.previous)
        print('clicked previous_btn')

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        self.child_frame = self.frames[page_name]
        self.child_frame.tkraise()

    # составляет список объектов для перелистывания в подменю
    def create_orders_set(self):
        orders_set = ()
        orders_dict = menu[self.order_type]
        for k,v in orders_dict.items():
            item = BaseOrderItem(**v)
            item.__name__ = k
            orders_set += (item,)
        return orders_set

    def get_orders_set(self):
        return self.frames_set


