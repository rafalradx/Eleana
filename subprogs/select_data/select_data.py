#!/usr/bin/python3
import pathlib
import pygubu
from modules.CTkListbox import *
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "select_data.ui"

class SelectData:
    def __init__(self, master=None, title=None, group=None, items=None):
        self.items = items
        self.master = master
        if title == None:
            title == ' '
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

       # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

        self.listFrame = builder.get_object("listFrame", master)
        self.selection_list = CTkListbox(self.listFrame, multiple_selection=True)
        self.selection_list.pack(fill="both", expand=True, padx=10, pady=10)

        self.group_field = builder.get_object("group_field", master)
        self.group_field.insert(0, group)
        self.group_field.configure(state="readonly")

        self.btn_ok = builder.get_object("btn_ok", master)

        # Set as modal
        self.mainwindow.grab_set()
        self.mainwindow.attributes('-topmost', True)
        self.mainwindow.title(title)

        # Keyboard bindings
        self.mainwindow.bind("<Escape>", self.cancel)
        self.mainwindow.bind("<Return>", lambda event: self.btn_ok.invoke())

        self.response = None

        self.selection_list.bind("<MouseWheel>", self.on_mousewheel)
        # Create available date
        i = 0
        for each in self.items:
            self.selection_list.insert(i, each)
            i += 1

    ''' DO NOT REMOVE GET AND RUN FUNCTIONS'''
    def get(self):
        ''' This function returns the output from the closed window'''
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def run(self):
        self.mainwindow.mainloop()

    def ok(self):
        ''' This is activated after clicking OK button'''
        self.response = self.selection_list.get()
        self.mainwindow.destroy()
    ''' END OF MANDATORY METHODS '''

    def deselect_all(self):
        i = 0
        while i < len(self.items):
            self.selection_list.deactivate(i)
            i += 1
    def select_all(self):
        i = 0
        while i < len(self.items):
            self.selection_list.activate(i)
            i += 1

    def ok(self):
        self.response = self.selection_list.get()
        self.mainwindow.destroy()
    def cancel(self, event = None):
        self.response = None
        self.mainwindow.destroy()

    def on_mousewheel(self, event):
        # Przewijaj listę przy użyciu kółka myszki
        if event.delta:
            print(event)
            #self.selection_list.yview_scroll(int(-1 * (event.delta / 120)), "units")

if __name__ == "__main__":
    app = SelectData()
    app.run()
