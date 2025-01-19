#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from DistanceReadui import DistanceReadUI


class DistanceRead(DistanceReadUI):
    def __init__(self, master=None):
        super().__init__(master)

    def track_minmax_clicked(self):
        pass

    def find_minmax_clicked(self):
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
    app = DistanceRead()
    app.run()
