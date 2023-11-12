#!/usr/bin/python3
import pathlib
import pygubu
from pandastable import Table

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "table.ui"


class CreateFromTable:
    def __init__(self, master=None, df = None, name = None, group = None):
        self.master = master
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

        if name:
            self.entry_name.insert(0, name)

        if group:
            self.entry_group.insert(0, group)

        self.pt = Table(self.tableFrame, dataframe = df, showtoolbar=True)
        self.pt.show()
    def run(self):
        self.mainwindow.mainloop()

if __name__ == "__main__":
    app = TableApp()
    pt = Table(app.tableFrame, showtoolbar=True)
    pt.show()
    app.run()
