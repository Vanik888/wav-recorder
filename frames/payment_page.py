# -*- coding: utf-8 -*-

from tkinter import Frame, PhotoImage, Button, Label
from frames.comon_frame_mixin import CommonFrameMixin
from frames.payment_table import PaymentTableFrame

class PaymentPage(Frame, CommonFrameMixin):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, kwargs['root'], **kwargs['frame_size'])
        self._root = kwargs['root']
        self._controller = kwargs['controller']
        self._frame_size = kwargs['frame_size']

        header_txt = 'Оплата заказа'

        btns_txt_len = 20

        self.header = Label(self, text=header_txt, anchor='se', font=("Helvetica", 16, "bold"))
        self.btn_font = self.get_bnt_font()

        self._child_frame_size = {'height': 380, 'width': 880}
        self.child_frame = PaymentTableFrame(root=self, frame_size=self._child_frame_size, data=self.get_data())

        total_price_txt = 'Итого: %s руб' % str(self.get_total_price())
        self.total_price_lbl = Label(self, text=total_price_txt, font=("Helvetica", 20, "bold"))

        self.pay_btn_img = PhotoImage(file='./stat/inteface_images/money.png')
        self.pay_btn = Button(self, text=self.add_spaces_to_str(btns_txt_len, 'Оплатить'), image=self.pay_btn_img, compound='right', font=self.btn_font)
        self.pay_btn.bind('<Button-1>', self.pay_ev)

        self.return_btn_img = PhotoImage(file='./stat/inteface_images/back.png')
        self.return_btn = Button(self, text=self.add_spaces_to_str(btns_txt_len, 'Назад'), image=self.return_btn_img, compound='right', font=self.btn_font)
        self.return_btn.bind('<Button-1>', self.return_ev)


        self.get_data()
        self.place_content()

    def get_data(self):
        data = []
        i = 0
        for p in self._controller.get_order_pages():
            for f in p.get_orders_set():
                if f.count > 0:
                    i += 1
                    data.append((i, f.name, f.count, f.price, f.get_full_price()))

        for v in data:
            print(v)
        return data

    def get_total_price(self):
        data = self.get_data()
        total = 0
        for p in self._controller.get_order_pages():
                    for f in p.get_orders_set():
                        if f.count > 0:
                            total += f.get_full_price()
        return total


    def place_content(self):
        click_btn_size = {'height': 90, 'width': 380}
        header_size = {'height': 40, 'width': 200}
        total_price_lbl_size = {'height': 70, 'width': 300}

        header_y_pad = 3
        header_x_pos = self._frame_size['width']/2 - header_size['width']/2 + 20
        self.header.place(x=header_x_pos, y=header_y_pad)

        self.child_frame.place(x=10, y=header_size['height']+2*header_y_pad)



        btns_y = self._frame_size['height'] - click_btn_size['height'] - 10
        self.total_price_lbl.place(x=10, y=(btns_y - total_price_lbl_size['height']), **total_price_lbl_size)

        self.pay_btn.place(x=10, y=btns_y, **click_btn_size)
        self.return_btn.place(x=(self._frame_size['width']-click_btn_size['width']-10), y=btns_y, **click_btn_size)

    def pay_ev(self, ev):
        print('clicked pay_btn')

    def return_ev(self, ev):
        print('clicked return_btn')
        self._controller.show_frame('StartPage')
        self.destroy()
