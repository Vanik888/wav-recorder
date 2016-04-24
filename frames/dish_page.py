# -*- coding: utf-8 -*-

from tkinter import Frame, Button, Label, PhotoImage
from frames.dish_image_frame import DishImageFrame

class DishPage(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, kwargs['root'], **kwargs['frame_size'])
        self._root = kwargs['root']
        self._controller = kwargs['controller']
        self._frame_size = kwargs['frame_size']


        self.header = Label(self, text='Выбор блюда', anchor='se', font=("Helvetica", 16, "bold"))
        image_path = './stat/inteface_images/Robot-icon.png'
        self.image = PhotoImage(file=image_path)

        self.speech_btn = Button(self, text='Говорите', image=self.image, compound='right')
        self.speech_btn.bind('<Button-1>', self.speech_ev)

        self.return_btn = Button(self, text='Назад', image=self.image, compound='right')
        self.return_btn.bind('<Button-1>', self.return_ev)

        self.add_btn = Button(self, text='Добавить', image=self.image, compound='right')
        self.add_btn.bind('<Button-1>', self.add_ev)

        self.remove_btn = Button(self, text='Убрать', image=self.image, compound='right')
        self.remove_btn.bind('<Button-1>', self.remove_ev)

        # поле с картинкой
        self.container = Frame(self)
        self._container_size = {'height': 400, 'width': 600}

        self.frames = {}
        for F in (DishImageFrame,):
            page_name = F.__name__
            frame = F(root=self.container, controller=self, frame_size=self._container_size)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            # frame.pack(side='top', fill='x')
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("DishImageFrame")


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



    def speech_ev(self, ev):
        print('clicked speech_btn')

    def return_ev(self, ev):
        print('clicked return_btn')
        self._controller.show_frame('StartPage')

    def add_ev(self, ev):
        print('clicked add_btn')

    def remove_ev(self, ev):
        print('clicked remove_btn')


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

