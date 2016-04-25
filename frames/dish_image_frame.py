# -*- coding: utf-8 -*-

from tkinter import Frame, PhotoImage, Label, Text

from frames.comon_frame_mixin import CommonFrameMixin

class DishImageFrame(Frame, CommonFrameMixin):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, kwargs['root'], background='green', **kwargs['frame_size'])
        self._root = kwargs['root']
        self._controller = kwargs['controller']
        self._frame_size = kwargs['frame_size']
        self.dish = kwargs['dish']()

        self.image = PhotoImage(file=self.dish.image_path)

        # self.dish_name_lbl = Text(self, text=self.dish.name, font=('Helvetica', 16, 'bold'), justify='left', wraplength=30, wrap='word', bg='white')
        self.dish_name_lbl = Label(self, text=self.get_name_formated_by_lines(20, self.dish.name), font=('Helvetica', 15, 'bold'), justify='left', anchor='n', bg='white')
        self.dish_img_lbl = Label(self, image=self.image, compound='right', bg='red')
        self.count_lbl = Label(self, text='0', font=('Helvetica', 44, 'bold'), bg='blue')

        self.place_content()

    def place_content(self):
        txt_lbl_size = {'height': 200, 'width': 250}
        image_lbl_size = {'height': 400, 'width': 300}
        count_lbl_size = {'height': 120, 'width': 250}
        x_diff = (self._frame_size['width'] - txt_lbl_size['width'] - image_lbl_size['width'])/3

        self.dish_name_lbl.place(x=x_diff, y=20, **txt_lbl_size)
        self.dish_img_lbl.place(x=txt_lbl_size['width'] + 2*x_diff, y=0)
        self.count_lbl.place(x=x_diff, y=self._frame_size['height']-count_lbl_size['height'])
        print('place_content')

    def add_dish(self):
        self.dish.count += 1
        self.update_dish_lbl(count=self.dish.count)

    def remove_dish(self):
        if self.dish.count > 0:
            self.dish -= 1
            self.update_dish_lbl(count=self.dish.count)

    def update_dish_lbl(self, count):
        self.count_lbl.config(text=str(self.dish.count))
