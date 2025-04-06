#!/usr/bin/python3
import pathlib
import customtkinter as ctk
import numpy as np
import pygubu
import pandas
from pandastable import MultipleValDialog
from pathlib import Path
from modules.CTkMessagebox import CTkMessagebox
from assets.DataClasses import Single2D
from tkinter import filedialog
from modules.tksheet import Sheet
import copy
from subprogs.edit_parameters.edit_parameters import EditParameters

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "edit_values_in_table.ui"

class EditValuesInTable:
    def __init__(self, eleana_app,
                 master=None,
                 list2D = None,
                 headers = None,
                 df = None,
                 name = None,
                 group = None,
                 loadOnStart = None,
                 window_title = None,
                 default_x_axis = None,
                 default_y_axis = None,
                 x_unit=None,
                 x_name=None,
                 y_unit=None,
                 y_name=None,
                 set_parameters=None):
        self.master = master
        self.eleana = eleana_app
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)
        if not window_title:
            window_title = 'Create data from table'

        # References
        self.tableFrame = builder.get_object("tableFrame", master)
        self.mainwindow.title(window_title)
        self.entry_name = builder.get_object("entry_name", master)
        self.entry_group = builder.get_object("entry_group", master)
        self.x_axis_name = builder.get_object("x_axis_name", master)
        self.x_axis_unit = builder.get_object("x_axis_unit", master)
        self.y_axis_name = builder.get_object("y_axis_name", master)
        self.y_axis_unit = builder.get_object("y_axis_unit", master)
        self.sel_x_axis = builder.get_object('sel_x_axis', master)
        self.sel_rey_axis = builder.get_object('sel_rey_axis', master)
        self.sel_imy_axis = builder.get_object('sel_imy_axis', master)


        ''' SWITCHING OFF THE FRAMES WITH FIELDS '''
        self.frame_1 = builder.get_object('frame_1', master)
        self.frame_2 = builder.get_object('frame_2', master)
        self.frame_3 = builder.get_object('frame_3', master)
        self.frame_1.grid_remove()
        self.frame_2.grid_remove()
        self.frame_3.grid_remove()

        # Take a list of parameters to add to the data.
        self.set_parameters = set_parameters

        if name:
            self.entry_name.insert(0, name)
        if group:
            self.entry_group.insert(0, group)
        if x_unit:
            self.x_axis_unit.insert(0, x_unit)
        if y_unit:
            self.y_axis_unit.insert(0, y_unit)
        if x_name:
            self.x_axis_name.insert(0, x_name)
        if y_name:
            self.y_axis_name.insert(0, y_name)

        self.headers = headers

        self.generate_table(df, list2D)

        self.response = None
        self.mainwindow.bind("<Escape>", self.cancel)
        self.table.bind("<<Paste>>", self.paste_event)
        if loadOnStart == 'excel':
            dialog = self.loadExcel()
            if dialog == 'cancel':
                self.cancel
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
        if self.set_parameters is None:
            data['parameters'] = {}
        else:
            data['parameters'] = copy.deepcopy(self.set_parameters)
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
        if np.iscomplexobj(data['y']):
            data['complex'] =  True
        spectrum = Single2D(data)
        self.eleana.dataset.append(spectrum)
        if show_info == True:
            info = CTkMessagebox(title="", message="The data was added to the dataset.", icon="info")

    def generate_table(self, df=None, list2D=None):
        if df is not None:
            self.table = Sheet(self.tableFrame)
            column_names = df.columns.tolist()
            table_data =  df.values.tolist()
            self.table.set_sheet_data(table_data)
            self.table.headers(column_names)
            self.table.grid(row=0, column=0, sticky="nswe")

            self.table.change_theme(ctk.get_appearance_mode())
            self.table.enable_bindings( "ctrl_select", "all", "right_click_popup_menu")
        elif list2D:
            self.table = Sheet(self.tableFrame)
            column_names = self.headers
            table_data = list2D
            self.table.set_sheet_data(table_data)
            self.table.headers(column_names)
            self.table.grid(row=0, column=0, sticky="nswe")

            self.table.change_theme(ctk.get_appearance_mode())
            self.table.enable_bindings("ctrl_select", "all", "right_click_popup_menu")
            return

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
