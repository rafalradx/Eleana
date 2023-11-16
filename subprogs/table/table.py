#!/usr/bin/python3
import pathlib
import pygubu
from pandastable import Table

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "table.ui"


class CreateFromTable:
    def __init__(self, eleana_app, master=None, df = None, name = None, group = None):
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
        self.mainwindow.title("Create data from table")
        self.entry_name = builder.get_object("entry_name", master)
        self.entry_group = builder.get_object("entry_group", master)
        self.x_axis_name = builder.get_object("x_axis_name", master)
        self.x_axis_unit = builder.get_object("x_axis_unit", master)
        self.y_axis_name = builder.get_object("y_axis_name", master)
        self.y_axis_unit = builder.get_object("y_axis_unit", master)
        self.sel_x_axis = builder.get_object('sel_x_axis', master)
        self.sel_rey_axis = builder.get_object('sel_rey_axis', master)
        self.sel_imy_axis = builder.get_object('sel_imy_axis', master)


        if name:
            self.entry_name.insert(0, name)
        if group:
            self.entry_group.insert(0, group)

        self.headers = ['None']
        self.headers.extend(df.columns)
        self.sel_x_axis.configure(values = self.headers)
        self.sel_rey_axis.configure(values=self.headers)
        self.sel_imy_axis.configure(values=self.headers)

        self.sel_x_axis.set(self.headers[1])
        self.sel_rey_axis.set(self.headers[2])
        self.sel_imy_axis.set(self.headers[0])

        self.table = Table(self.tableFrame, dataframe = df, showtoolbar=True)
        self.table.show()

        self.response = None

        self.mainwindow.bind("<Escape>", self.cancel)
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
        print("Ok")

if __name__ == "__main__":
    app = CreateFromTable()
    app.run()
