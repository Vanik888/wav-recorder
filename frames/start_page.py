# -*- coding: utf-8 -*-


from tkinter import Button, PhotoImage, Frame


class StartPage(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, kwargs['root'], **kwargs['frame_size'])
        self._root = kwargs['root']
        self._controller = kwargs['controller']
        self._frame_size = kwargs['frame_size']


        self.buttons_size = {'height': 80, 'width': 400}
        self.x_pos = (self._frame_size['width'] - self.buttons_size['width']) / 2
        self.y_diff = (self._frame_size['height'] - self.buttons_size['height'] * 4) / 5
        image_path = './stat/inteface_images/Robot-icon.png'
        self.image = PhotoImage(file=image_path)


        self.dishes_btn = Button(self, text='Выбор блюд', image=self.image, compound='right')
        self.dishes_btn.bind('<Button-1>', self.choose_dishes_ev)

        self.drinks_btn = Button(self, text='Выбор напитка', image=self.image, compound='right')
        self.drinks_btn.bind('<Button-1>', self.choose_drinks_ev)

        self.service_btn = Button(self, text='Сервис', image=self.image, compound='right')
        self.service_btn.bind('<Button-1>', self.choose_service_ev)

        self.bill_btn = Button(self, text='Оплата', image=self.image, compound='right')
        self.bill_btn.bind('<Button-1>', self.choose_bill_ev)

        self.place_content()

    def place_content(self):
        self.dishes_btn.place(x=self.x_pos , y=self.y_diff, **self.buttons_size)
        self.drinks_btn.place(x=self.x_pos, y=2*self.y_diff+self.buttons_size['height'], **self.buttons_size)
        self.service_btn.place(x=self.x_pos, y=3*self.y_diff+2*self.buttons_size['height'], **self.buttons_size)
        self.bill_btn.place(x=self.x_pos, y=4*self.y_diff+3*self.buttons_size['height'], **self.buttons_size)

    # кликнули на выбор блюда
    def choose_dishes_ev(self, ev):
        print('clicked dishes_btn: %s' % self.dishes_btn.config('text')[-1])
        self._controller.show_frame("DishPage")


    # кликнули на выбор напитка
    def choose_drinks_ev(self, ev):
        print('clicked dishes_btn: %s' % self.drinks_btn.config('text')[-1])

    # кликнули на выбор сервиса
    def choose_service_ev(self, ev):
        print('clicked dishes_btn: %s' % self.service_btn.config('text')[-1])

    # кликнули на выбор счета
    def choose_bill_ev(self, ev):
        print('clicked dishes_btn: %s' % self.bill_btn.config('text')[-1])

