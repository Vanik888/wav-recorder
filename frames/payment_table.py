# -*- coding: utf-8 -*-

import tkinter.font as tkFont

from tkinter import PhotoImage, Label, Frame
from tkinter.ttk import Treeview, Scrollbar, Frame as ttkFrame

from frames.comon_frame_mixin import CommonFrameMixin

class PaymentTableFrame(Frame, CommonFrameMixin):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, kwargs['root'], **kwargs['frame_size'])
        self._root = kwargs['root']
        self._frame_size = kwargs['frame_size']

        self.container = ttkFrame(master=self)
        self.data = kwargs['data']
        self.table_header = ['№', 'Наименование', 'Шт', 'Цена за штуку', 'Общая цена']


        self.table_tree = Treeview(self, columns=self.table_header, show='headings')
        self.vsb = Scrollbar(self, orient="vertical", command=self.table_tree.yview)

        self.table_tree.configure(yscrollcommand=self.vsb.set)
        self.label = Label(self, text='azaa', bg='white')

        self.place_content()
        self._build_tree()

    def place_content(self):
        vsb_size = {'width': 20, 'height': self._frame_size['height']}
        table_size = {'width': self._frame_size['width'] - vsb_size['width'], 'height': self._frame_size['height'] }
        self.table_tree.place(x=0, y=0, **table_size)
        self.vsb.place(x=table_size['width'], y=0, **vsb_size)


        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col in self.table_header:
            self.table_tree.heading(col, text=col.title(),
                command=lambda c=col: self.sortby(self.table_tree, c, 0))
            # adjust the column's width to the header string
            self.table_tree.column(col,
                width=tkFont.Font().measure(col.title()))
        for item in self.data:
            self.table_tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.table_tree.column(self.table_header[ix],width=None)<col_w:
                    self.table_tree.column(self.table_header[ix], width=col_w)


    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        #data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, \
            int(not descending)))

