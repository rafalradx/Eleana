#!/usr/bin/python3
import pathlib
import pygubu
import pandas
from assets.Parameter_dictionary import parameter_dictionary
from modules.tksheet import Sheet

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "edit_parameters.ui"

class EditParameters:
    def __init__(self, master=None, parameters = None, name = None):
        self.master = master
        self.builder = builder = pygubu.Builder()
        self.parameters = parameters

        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

        #screen_width = self.mainwindow.winfo_screenwidth()
        #screen_height = self.mainwindow.winfo_screenheight()
        screen_width = 1100
        screen_height = 600
        self.mainwindow.geometry(f"{screen_width}x{screen_height}")

        # References
        self.tableFrame = builder.get_object("tableFrame", master)
        self.mainwindow.title("Edit parameters")
        self.entry_name = builder.get_object('entry_name', master)

        if name:
            self.entry_name.insert(0, name)

        column_parameters = list(self.parameters.keys())
        column_values = list(self.parameters.values())
        column_description = self.create_description_for_parameters(column_parameters)

        df = pandas.DataFrame({'COMMENT': column_description, 'PARAMETER': column_parameters, 'VALUES': column_values},
                          columns=['COMMENT', 'PARAMETER', 'VALUES'])
        df['VALUES'] = df['VALUES'].astype(str)
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
        par_keys = self.table.get_column_data(1,
                                                get_displayed = False,
                                                get_header = False,
                                                get_header_displayed = False,
                                                only_rows = None)
        par_values = self.table.get_column_data(2,
                                                get_displayed = False,
                                                get_header = False,
                                                get_header_displayed = False,
                                                only_rows = None)
        parameters = {}
        i = 0
        while i < len(par_keys):
            parameters[par_keys[i]] = par_values[i]
            i += 1
        self.response = parameters
        self.mainwindow.destroy()

    def generate_table(self, df):
        self.table = Sheet(self.tableFrame)
        column_names = df.columns.tolist()
        table_data =  df.values.tolist()
        self.table.set_sheet_data(table_data)
        self.table.headers(column_names)
        self.table.grid(row=0, column=0, sticky="nswe")
        self.table.change_theme("dark")
        self.table.enable_bindings( "ctrl_select", "all", "right_click_popup_menu")
        self.table.set_options(50)
        self.table.highlight_columns(columns = [0], bg = '#2A578F', fg = None, highlight_header = True, redraw = True, overwrite = True)
        self.table.column_width(column = 0, width = 600, only_set_if_too_small = True, redraw = True)

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

    def create_description_for_parameters(self,column_parameters):
        column_descriptions = []
        for each in column_parameters:
            descr = parameter_dictionary.get(each, 'Custom parameter')
            column_descriptions.append(descr)
        return column_descriptions

if __name__ == "__main__":
    app = CreateFromTable()
    app.run()
