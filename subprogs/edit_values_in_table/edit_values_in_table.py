#!/usr/bin/python3
import pathlib
import customtkinter as ctk
import numpy as np
import pygubu
import string
from modules.CTkMessagebox import CTkMessagebox
from assets.DataClasses import Single2D
from modules.tksheet import Sheet
import copy
from assets.Error import Error

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "edit_values_in_table.ui"

class EditValuesInTable:
    def __init__(self, eleana_app, master,
                    x,                      # X array as 1D of np.array type
                    y,                      # Y array as 1D or 2D np.array type
                    name = None,            # The name of the currently edited data
                    column_names = None,    # The column headers if None will be default
                    window_title = None,    # The title of the window. If none it will be default
                    complex = None          # Are the data complex? If None, it will be determined automatically
                 ):

        self.master = master
        self.eleana = eleana_app
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        self.mainwindow.geometry("800x900")
        builder.connect_callbacks(self)
        if not window_title:
            window_title = 'Edit data in table'

        # References
        self.tableFrame = builder.get_object("tableFrame", master)
        self.mainwindow.title(window_title)

        ''' SWITCHING OFF THE FRAMES WITH FIELDS '''
        self.frame_1 = builder.get_object('ctkframe8', master)
        self.frame_2 = builder.get_object('ctkframe12', master)
        self.frame_3 = builder.get_object('ctkframe4', master)
        self.frame_1.grid_remove()
        self.frame_2.grid_remove()
        self.frame_3.grid_remove()

        # Create data for table:
        self.row_counts = len(x)
        x_data = np.atleast_1d(x)
        if len(y.shape) == 0:
            self.column_counts = 2
        else:
            self.column_counts = y.shape[0]
        print(f"wiersze = {self.row_counts}")
        print(f"kolumny = {self.column_counts}")
        y_data = np.atleast_2d(y).T

        if complex is None:
            self.complex = np.iscomplexobj(y_data)
        else:
            self.complex = complex
        list2D = [[x_data[i], *y_data[i]] for i in range(0, len(x_data))]
        if not column_names:
            column_names = []
            n = len(list2D[0])
            for i in range(0, n):
                label = ""
                while i >= 0:
                    label = string.ascii_uppercase[i % 26] + label
                    i = i // 26 - 1
                column_names.append(label)
        self.generate_table(column_names, list2D)

        self.response = None
        self.mainwindow.bind("<Escape>", self.cancel)
        self.table.bind("<<Paste>>", self.paste_event)
        self.mainwindow.attributes('-topmost', True)

    def get(self):
        if self.mainwindow.winfo_exists():
           self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event = None):
        self.response = None
        self.mainwindow.destroy()

    def run(self):
        self.mainwindow.mainloop()

    def ok(self):
        self.prepare_results()
        self.mainwindow.destroy()

    def prepare_results(self):
        row_counts = self.row_counts
        column_counts = self.column_counts
        data = []
        for n in range(row_counts):
            row_data = []
            for m in range(column_counts):
                cell_value = self.table.get_cell_data(n, m)
                try:
                    # Check if values for y are complex
                    if isinstance(cell_value, complex):
                        row_data.append(cell_value)
                    else:
                        # The value is not complex
                        row_data.append(float(cell_value))
                except ValueError:
                    Error.show(info = f"Could not convert data in cell ({i}, {j}) to a number: {cell_value}")
                    return None
            data.append(row_data)
        return np.array(data)

    def generate_table(self, headers, list2D):
        self.table = Sheet(self.tableFrame)
        self.table.set_sheet_data(list2D)
        self.table.headers(headers)
        self.table.grid(row=0, column=0, sticky="nswe")
        self.table.change_theme(ctk.get_appearance_mode())
        self.table.enable_bindings("ctrl_select", "all", "right_click_popup_menu")

    def get_data_from_column(self, column_name):
        index = self.sel_x_axis._values.index(column_name)
        if index < 0:
            return
        column_data = self.table.get_column_data(index - 1)
        return column_data

    def paste_event(self, event):
        data = self.mainwindow.clipboard_get()
        rows = data.split('\n')
        nrows = len(rows)
        ncols = max(len(row.split('\t')) for row in rows)
        self.table.set_sheet_data([[None] * ncols] * nrows)

if __name__ == "__main__":
    app = CreateFromTable()
    app.run()
