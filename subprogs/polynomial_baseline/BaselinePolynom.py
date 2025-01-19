#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from BaselinePolynomui import BaselinePolynomUI


class BaselinePolynom(BaselinePolynomUI):
    def __init__(self, master=None):
        super().__init__(master)

    def keep_current_baseline(self):
        pass

    def ok_clicked(self):
        pass

    def show_report_clicked(self):
        pass

    def process_group_clicked(self):
        pass

    def clear_report_clicked(self):
        pass

    def cancel(self):
        pass


if __name__ == "__main__":
    app = BaselinePolynom()
    app.run()
