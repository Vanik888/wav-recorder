# -*- coding: utf-8 -*-

from tkinter import Frame, PhotoImage, Label

class DishImageFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, kwargs['root'], **kwargs['frame_size'])
        self._root = kwargs['root']
        self._controller = kwargs['controller']
        self._frame_size = kwargs['frame_size']
        self.dish = kwargs['dish']()

        self.image = PhotoImage(file=self.dish.image_path)

        self.dish_img_lbl = Label(self, text=self.dish.name, image=self.image, compound='right')

        self.count_lbl = Label(self, text='0')

        self.place_content()

    def place_content(self):
        self.dish_img_lbl.place(x=10, y=10)
        self.count_lbl.place(x=0, y=0)
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
