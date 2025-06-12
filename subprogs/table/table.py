#!/usr/bin/python3
import pathlib
import customtkinter as ctk
import numpy as np
import pygubu
import pandas
from pathlib import Path
from modules.CTkMessagebox import CTkMessagebox
from assets.DataClasses import BaseDataModel
from tkinter import filedialog
from modules.tksheet import Sheet
import copy
from subprogs.edit_parameters.edit_parameters import EditParameters

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "table.ui"

class CreateFromTable:
    def __init__(self, eleana_app,
                 master=None,
                 list2D = None,
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
        self.edit_frame = builder.get_object('ctkframe4', master)
        self.edit_frame.grid_remove()

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

        self.headers = ['None']
        self.headers.extend(df.columns)

        self.sel_x_axis.configure(values = self.headers)
        self.sel_rey_axis.configure(values=self.headers)
        self.sel_imy_axis.configure(values=self.headers)
        self.sel_x_axis.set(self.headers[1])
        self.sel_rey_axis.set(self.headers[2])
        self.sel_imy_axis.set(self.headers[0])
        if default_x_axis:
            self.sel_x_axis.set(default_x_axis)
        if default_y_axis:
            self.sel_rey_axis.set(default_y_axis)
        self.generate_table(df, list2D)

        self.response = None
        self.mainwindow.bind("<Escape>", self.cancel)
        self.table.bind("<<Paste>>", self.paste_event)
        if loadOnStart == 'excel':
            dialog = self.loadExcel()
            if dialog == 'cancel':
                self.cancel
        self.mainwindow.attributes('-topmost', True)

    def loadExcel(self):
        self.mainwindow.iconify()
        filename = filedialog.askopenfilename(parent=self.mainwindow,
                                              defaultextension='.xls',
                                              title = "Import Excel/LibreOffice Calc",
                                              filetypes=[("xlsx", "*.xlsx"),
                                                         ("xls", "*.xls"),
                                                         ("ods", "*.ods"),
                                                         ("All files", "*.*")])
        if len(filename) == 0:
            self.cancel()
            return 'cancel'

        self.eleana.paths['last_import_dir'] = str(Path(filename).parent)
        name = str(Path(filename).name)
        self.entry_group.insert(0, 'All')
        self.mainwindow.deiconify()
        self.entry_name.delete(0, "end")
        self.entry_name.insert(0, name)
        xl = pandas.ExcelFile(filename)
        names = xl.sheet_names
        d = MultipleValDialog(title='Import Sheet',
                              initialvalues=([names]),
                              labels=(['Sheet']),
                              types=(['combobox']),
                              parent=self.mainwindow)
        if not d.result:
            return
        df = xl.parse(d.results[0])
        df = df.map(lambda x: round(float(x), 8)).astype(object)
        self.generate_table(df)
        self.headers = ['None']
        col_names = df.columns.tolist()
        self.headers.extend(col_names)
        self.sel_x_axis.configure(values=self.headers)
        self.sel_rey_axis.configure(values=self.headers)
        self.sel_imy_axis.configure(values=self.headers)
        try:
            self.sel_imy_axis.set(self.headers[0])
        except:
            pass
        try:
            self.sel_x_axis.set(self.headers[1])
        except:
            pass
        try:
            self.sel_rey_axis.set(self.headers[2])
        except:
            pass

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

        x_data = self.get_data_from_column(x_column)
        rey = self.get_data_from_column(rey_column)
        if isinstance(x_data, str):
            info = CTkMessagebox(title="", message=x_data, icon="cancel")
            return
        elif isinstance(rey, str):
            info = CTkMessagebox(title="", message=rey, icon="cancel")
            return
        if rey.size != x_data.size:
            info = CTkMessagebox(title="", message="X and Y tables have different lenght.", icon="cancel")
            return
        data['y'] = rey
        data['x'] = x_data

        if imy_column == 'None':
            data['complex'] = False
        else:
            data['complex'] = True
            imy = self.get_data_from_column(imy_column)
            if isinstance(imy, str):
                info = CTkMessagebox(title="", messaage=imy, icon="cancel")
                return
            elif imy.size != reY.size:
                info = CTkMessagebox(title="", message="ReY and ImY tables have different lenght.", icon="cancel")
                return
            data_complex = rey + 1j * imy
            data['y'] = data_complex
        data['type'] = 'single 2D'
        data['origin'] = 'imported'
        if np.iscomplexobj(data['y']):
            data['complex'] =  True
        spectrum = BaseDataModel.from_dict(data)
        self.eleana.dataset.append(spectrum)
        if show_info == True:
            info = CTkMessagebox(title="", message="The data was added to the dataset.", icon="info")

    def edit_parameters(self):
        if not self.set_parameters:
            self.set_parameters = {
                'name_x': self.x_axis_name.get(),
                'unit_x': self.x_axis_unit.get(),
                'name_y': self.y_axis_name.get(),
                'unit_y': self.y_axis_unit.get()
            }
        edit_par = EditParameters(master = self.mainwindow, parameters=self.set_parameters)
        self.set_parameters = edit_par.get()

        self.x_axis_name.delete(0, "end")
        self.x_axis_name.insert(0, self.set_parameters['name_x'])

        self.x_axis_unit.delete(0, "end")
        self.x_axis_unit.insert(0, self.set_parameters['unit_x'])

        self.y_axis_name.delete(0, "end")
        self.y_axis_name.insert(0, self.set_parameters['name_y'])

        self.y_axis_unit.delete(0, "end")
        self.y_axis_unit.insert(0, self.set_parameters['unit_y'])

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
            print('table.py - generate_table')
            return

    def get_data_from_column(self, column_name):
        index = self.sel_x_axis._values.index(column_name)
        if index < 0:
            return
        column_data = self.table.get_column_data(index - 1)
        filtered_data = [x.strip() if isinstance(x, str) else x for x in column_data]
        floats_data = []
        for each in filtered_data:
            try:
                floats_data.append(float(each))
            except ValueError:
                error = f"There is non-numeric value: {each} in the table."
                return error
        column_data = np.array(floats_data)
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
