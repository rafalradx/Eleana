#!/usr/bin/python3
import pathlib
from tkinter import Event
import pygubu
from modules.CTkMessagebox.ctkmessagebox import CTkMessagebox
PROJECT_PATH = pathlib.Path(__file__).parent

# Adjust the name of the file with UI
PROJECT_UI = PROJECT_PATH / "add_group.ui"

class Groupcreate:
    def __init__(self, master = None, eleana_instance = None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)
        # Reference to master window and eleana instance and response variable
        self.group_name_entry = builder.get_object("ctkentry2", self.mainwindow)
        self.description = builder.get_object("ctkentry3", self.mainwindow)
        self.btn_create = builder.get_object("btn_create", self.mainwindow)
        self.master = master
        self.eleana = eleana_instance
        self.response = None
        ''' Do not modify the code until this part'''

        # Set the window properties to modal mode
        self.master.update()
        self.mainwindow.attributes('-topmost', True)  # Always on top
        self.mainwindow.title('Create new group')

        #self.group_name_entry.focus_set()
        # Define keyboard bindings
        self.mainwindow.bind('<Return>', lambda event: self.btn_create.invoke())
        self.mainwindow.bind("<Escape>", self.cancel)

    ''' DO NOT REMOVE GET AND RUN FUNCTIONS'''
    def get(self):
        if self.mainwindow.winfo_exists():
           self.master.wait_window(self.mainwindow)
        return self.response
    def run(self):
        self.mainwindow.mainloop()
    ''' END OF MANDATORY METHODS '''

    def create_group(self):
        groups = list(self.eleana.assignmentToGroups.keys())
        new_group = self.group_name_entry.get()
        if new_group not in groups:
            self.eleana.assignmentToGroups[new_group] = []
            self.group_name_entry.delete(0, "end")
            self.description.delete(0, "end")
            self.cancel(None)
        else:
            info = "The group '" + new_group + "' already exists! Please choose different name."
            CTkMessagebox(title="", message=info, icon = "cancel")
        self.response = new_group

    def cancel(self, event: Event = None):
        self.master.attributes('-topmost', True)
        self.mainwindow.destroy()

if __name__ == "__main__":
    app = Groupcreate()
    app.run()

