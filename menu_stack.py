# -*- coding: utf-8 -*-

import tkinter as tk   # python3
#import Tkinter as tk   # python
from tkinter import Tk
from tkinter import Frame

from frames.start_page import StartPage
from frames.dish_page import DishPage
from frames.speech_page import SpeechPage

TITLE_FONT = ("Helvetica", 18, "bold")
frame_size = {'height': 600, 'width': 900}

class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, DishPage, SpeechPage):
            page_name = F.__name__
            frame = F(root=container, controller=self, frame_size=frame_size)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            # frame.pack(side='top', fill='x')
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
