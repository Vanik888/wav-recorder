# -*- coding: utf-8 -*-

import tkinter as tk   # python3
#import Tkinter as tk   # python
from tkinter import Tk
from tkinter import Frame

from frames.start_page import StartPage
from frames.dish_page import DishPage
from frames.drinks_page import DrinksPage
from frames.services_page import ServicesPage
from frames.speech_page import SpeechPage
from frames.payment_page import PaymentPage

TITLE_FONT = ("Helvetica", 18, "bold")
frame_size = {'height': 600, 'width': 900}

class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.current_frame = None

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, DishPage, DrinksPage, ServicesPage, PaymentPage, SpeechPage):
            page_name = F.__name__
            frame = F(root=self.container, controller=self, frame_size=frame_size)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            # frame.pack(side='top', fill='x')
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if page_name == 'SpeechPage':
            self.frames['SpeechPage'] = SpeechPage(root=self.container, controller=self, frame_size=frame_size)
            self.frames['SpeechPage'].grid(row=0, column=0, sticky="nsew")
        elif page_name == 'PaymentPage':
            self.frames['PaymentPage'] = PaymentPage(root=self.container, controller=self, frame_size=frame_size)
            self.frames['PaymentPage'].grid(row=0, column=0, sticky="nsew")


        self.current_frame = self.frames[page_name]
        self.current_frame.tkraise()

    def get_order_pages(self):
        return [self.frames['DishPage'], self.frames['DrinksPage'], self.frames['ServicesPage']]

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
