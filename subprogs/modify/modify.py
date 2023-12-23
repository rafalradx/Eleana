#!/usr/bin/python3
import pathlib
import pygubu
import tkinter as tk
from tkinter import ttk
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "modify.ui"

class ModifyData:
    def __init__(self, master, eleana=None, grapher=None, app=None ):
        # References to the main objects
        self.eleana = eleana
        self.grapher = grapher
        self.app = app
        self.master = master

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # Main widget
        self.mainwindow = builder.get_object("toplevel1", self.master)
        self.mainwindow.title("Modify")
        self.mainwindow.attributes('-topmost', True)

        # References to widgets
        self.sel_x_oper = builder.get_object("sel_x_oper", master)
        self.sel_y_oper = builder.get_object("sel_y_oper", master)
        self.sel_z_oper = builder.get_object("sel_z_oper", master)
        self.spinbox_x = builder.get_object("spinbox_x", master)
        self.spinbox_y = builder.get_object("spinbox_y", master)
        self.spinbox_z = builder.get_object("spinbox_z", master)

        self.sel_x_oper.set("None")
        self.sel_y_oper.set("None")
        self.sel_z_oper.set("None")

        self.r1 = builder.get_object("r1", master)
        self.r2 = builder.get_object("r2", master)
        self.r3 = builder.get_object("r3", master)
        self.r4 = builder.get_object("r4", master)
        self.r5 = builder.get_object("r5", master)
        self.r6 = builder.get_object("r6", master)
        self.r7 = builder.get_object("r7", master)
        self.r8 = builder.get_object("r8", master)
        self.r9 = builder.get_object("r9", master)

        # Radiobuttons
        self.step = tk.DoubleVar()
        builder.import_variables(self, ['step'])
        builder.connect_callbacks(self)

        # Set staring values for spinboxes
        self.set_spinbox_starting_value()
        self.r5.select()

        self.response = None
        # Add tracing of selections
        #self.first = tk.DoubleVar(master=self.app, value=self.eleana.selections['first'])
        #self.first.trace(mode='w', callback=self.first_changed)

    def get(self):
        if self.mainwindow.winfo_exists():
           self.master.wait_window(self.mainwindow)
        return self.response
    def cancel(self, event = None):
        self.response = None
        self.mainwindow.destroy()
    def run(self):
        self.mainwindow.mainloop()

    def first_changed(self, name, index, mode):
        print("zmieniono")
    def set_step(self):
        current_step = self.step.get()
        self.spinbox_x.config(increment = current_step)
        self.spinbox_y.config(increment=current_step)
        self.spinbox_z.config(increment=current_step)

        print(current_step)
    def ok_clicked(self):
        pass

    def set_spinbox_starting_value(self):
        self.spinbox_x.set(1)
        self.spinbox_y.set(1)
        self.spinbox_z.set(1)

if __name__ == "__main__":
    app = ModifyData()
    app.run()
