# -*- coding: utf-8 -*-

from tkinter import Frame, PhotoImage, Label

from frames.comon_frame_mixin import CommonFrameMixin

class DishImageFrame(Frame, CommonFrameMixin):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, kwargs['root'], background='green', **kwargs['frame_size'])
        self._root = kwargs['root']
        self._controller = kwargs['controller']
        self._frame_size = kwargs['frame_size']
        self.dish = kwargs['dish']

        self.image = PhotoImage(file=self.dish.image_path)

        dish_lbl_txt_length = 18
        self.dish_name_lbl = Label(self, text=self.get_name_formated_by_lines(dish_lbl_txt_length, self.dish.name), font=('Helvetica', 16, 'bold'), anchor='n', bg='white')
        self.dish_description_lbl = Label(self, text=self.get_name_formated_by_lines(dish_lbl_txt_length, self.dish.description), font=('Helvetica', 14), anchor='n')
        self.dish_price_lbl = Label(self, text='0 Руб', anchor='nw', font=('Helvetica', 14))
        self.count_lbl = Label(self, text='0', font=('Helvetica', 44, 'bold'), bg='blue')
        self.dish_img_lbl = Label(self, image=self.image, compound='right', bg='red')

        self.place_content()

    def place_content(self):
        name_lbl_size = {'height': 80, 'width': 250}
        image_lbl_size = {'height': 400, 'width': 300}
        description_size = {'height': 120, 'width': 250}
        price_lbl_size = {'height': 40, 'width': 250}
        count_lbl_size = {'height': 90, 'width': 250}

        x_diff = (self._frame_size['width'] - name_lbl_size['width'] - image_lbl_size['width'])/3

        self.dish_name_lbl.place(x=x_diff, y=20, **name_lbl_size)
        self.dish_img_lbl.place(x=name_lbl_size['width'] + 2*x_diff, y=0)
        self.dish_description_lbl.place(x=x_diff, y=20+name_lbl_size['height'] + 5, **description_size)
        self.dish_price_lbl.place(x=x_diff, y=20+name_lbl_size['height'] + 5 + description_size['height'] + 5, **price_lbl_size)
        self.count_lbl.place(x=x_diff, y=self._frame_size['height']-count_lbl_size['height'])

    def add_dish(self):
        self.dish.count += 1
        self.update_dish_lbl(count=self.dish.count)

    def remove_dish(self):
        if self.dish.count > 0:
            self.dish.count -= 1
            self.update_dish_lbl(count=self.dish.count)

    def update_dish_lbl(self, count):
        self.dish_price_lbl.config(text=str(count*self.dish.price) + ' Руб')
        self.count_lbl.config(text=str(count))
