#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from normalize.Normalizeui import NormalizeUI

class Normalize(NormalizeUI):
    def __init__(self, master=None):
        super().__init__(master)
        self.mainwindow.title('Normalize amplitude')
        self.mainwindow.attributes('-topmost', False)

        self.spinboxFrame = self.builder.get_object('spinboxFrame', self.mainwindow)
        self.spinbox = self.builder.get_object('spinbox', self.mainwindow)

    ''' STANDARD METHODS TO HANDLE WINDOW BEHAVIOR '''
    def get(self):
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event=None):
        ''' Close the window without changes '''
        self.response = None
        self.mainwindow.destroy()

    def ok_clicked(self):
        pass


    def process_group(self):
        pass


if __name__ == "__main__":
    app = Normalize()
    app.run()
