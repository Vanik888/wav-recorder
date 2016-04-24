# -*- coding: utf-8 -*-

from tkinter import Frame, PhotoImage, Label

class DishImageFrame(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, kwargs['root'], **kwargs['frame_size'])
        self._root = kwargs['root']
        self._controller = kwargs['controller']
        self._frame_size = kwargs['frame_size']



        image_path = './stat/inteface_images/krep_klubnichno_orekhoviy.png'
        self.image = PhotoImage(file=image_path)

        self.dish_img_lbl = Label(self, text='Клубничная вкусняшка', image=self.image, compound='right')


        self.place_content()

    def place_content(self):
        self.dish_img_lbl.place(x=10, y=10)
        print('place_content')
