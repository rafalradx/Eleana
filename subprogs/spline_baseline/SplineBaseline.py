#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from SplineBaselineui import SplineBaselineUI


class SplineBaseline(SplineBaselineUI):
    def __init__(self, master=None):
        super().__init__(master)

    def sel_polynomial_clicked(self, value):
        pass

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
    app = SplineBaseline()
    app.run()
