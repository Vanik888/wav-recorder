# -*- coding: utf-8 -*-

from tkinter import Frame, Button, Label

class DishFrame():
    def __init__(self, *args, **kwargs):
        self._root = kwargs['root']

        self.frame = Frame(self._root, height=480, width=640)
        self.header = Label(self._root, text='Выбор блюда')

        self.place_content()

    def place_content(self):
        self.header.pack(side='top', fill='x')
