#!/usr/bin/python3
import pathlib

import numpy as np
import pygubu
import pandas
from pandastable import Table, MultipleValDialog
from pathlib import Path
from modules.CTkMessagebox import CTkMessagebox
from assets.DataClasses import Single2D
from tkinter import filedialog
from modules.tksheet import Sheet

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "edit_parameters.ui"

class EditParameters:
    def __init__(self, eleana_app, master=None, index = None):
        self.master = master
        self.eleana = eleana_app
        self.builder = builder = pygubu.Builder()

        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

        # References
        self.tableFrame = builder.get_object("tableFrame", master)
        self.mainwindow.title("Edit parameters")
        self.entry_name = builder.get_object('entry_name', master)

        self.index_of_data = index
        self.data_to_edit = self.eleana.dataset[self.index_of_data]
        name = self.data_to_edit.name_nr
        if name:
            self.entry_name.insert(0, name)

        headers = ['PARAMETER', 'VALUE']
        parameters = self.data_to_edit.parameters
        self.stk_names  = self.data_to_edit.parameters.get('stk_names', None)
        if self.stk_names != None:
            parameters.pop('stk_names')
        df = pandas.DataFrame(list(parameters.items()), columns=headers )

        self.generate_table(df)
        self.response = None
        self.mainwindow.bind("<Escape>", self.cancel)
        self.table.bind("<<Paste>>", self.paste_event)

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
        self.add_to_dataset(False)
        self.mainwindow.destroy()

    def add_to_dataset(self, show_info=True):
        x_column = self.sel_x_axis.get()
        rey_column = self.sel_rey_axis.get()
        imy_column = self.sel_imy_axis.get()
        if x_column == 'None' or rey_column == 'None':
            info = CTkMessagebox(title = "", message="Please select columns for X and Y axis.", icon = "info")
            return

        data = {}
        data['parameters'] = {}
        data['name'] = self.entry_name.get()
        if self.entry_group.get():
            data['groups'] = [self.entry_group.get()]
        else:
            data['groups'] = ['All']
        data['parameters']['name_x'] = self.x_axis_name.get()
        data['parameters']['name_y'] = self.y_axis_name.get()
        data['parameters']['unit_x'] = self.x_axis_unit.get()
        data['parameters']['unit_y'] = self.y_axis_unit.get()

        data['x'] = self.get_data_from_column(x_column)
        rey = np.array(self.get_data_from_column(rey_column))
        data['y'] = rey

        if imy_column == 'None':
            data['complex'] = False
        else:
            data['complex'] = True
            imy = self.get_data_from_column(imy_column)
            imy = np.array(imy)
            data_complex = rey + 1j * imy
            data['y'] = data_complex
        data['type'] = 'single 2D'
        data['origin'] = 'imported'
        spectrum = Single2D(data)
        self.eleana.dataset.append(spectrum)
        if show_info == True:
            info = CTkMessagebox(title="", message="The data was added to the dataset.", icon="info")

    def generate_table(self, df):
        self.table = Sheet(self.tableFrame)
        column_names = df.columns.tolist()
        table_data =  df.values.tolist()
        self.table.set_sheet_data(table_data)
        self.table.headers(column_names)
        self.table.grid(row=0, column=0, sticky="nswe")
        self.table.change_theme("dark")
        self.table.enable_bindings( "ctrl_select", "all", "right_click_popup_menu")

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
