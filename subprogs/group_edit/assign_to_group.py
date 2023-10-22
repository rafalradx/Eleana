#!/usr/bin/python3
import pathlib
import pygubu
from CTkMessagebox import CTkMessagebox
from subprogs.group_edit.add_group import Groupcreate
PROJECT_PATH = pathlib.Path(__file__).parent

# Adjust the name of the file with UI
PROJECT_UI = PROJECT_PATH / "assign_to_group.ui"

class Groupassign:
    def __init__(self, master = None, eleana_instance = None, which = 'first'):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        self.master = master.mainwindow
        self.eleana = eleana_instance
        self.response = None
        self.app = master

        #if self.eleana != None:
        #     if self.eleana.selections['first'] < 0:
        #         exit()

                # Main widget
        self.mainwindow = builder.get_object("toplevel1", self.master)
        builder.connect_callbacks(self)
        # Reference to master window and eleana instance and response variable

        ''' Do not modify the code until this part'''


        # Set the window properties to modal mode
        self.mainwindow.grab_set()  # Set as modal
        self.mainwindow.attributes('-topmost', True)  # Always on top
        self.mainwindow.title('Add new group')


        # Define references to objects in the window
        # --- example: self.text_box contains textbox widget object
        self.btn_to_existing = builder.get_object("btn_to_existing", self.mainwindow)
        self.btn_new = builder.get_object("btn_new", self.mainwindow)
        self.btn_cancel = builder.get_object("btn_cancel", self.mainwindow)
        self.sel_group = builder.get_object("sel_group", self.mainwindow)
        self.name_label = builder.get_object('ctklabel1', self.mainwindow)

        first_list = self.app.sel_first._values
        label_text = 'Assign:   ' + self.app.sel_first.get()
        self.name_label.configure(text = label_text)

        groups = list(self.eleana.assignmentToGroups.keys())
        self.sel_group.configure(values = groups)
        self.sel_group.set('All')
        #self.mainwindow.bind('<Return>', lambda event: self.btn_create.invoke())

    ''' DO NOT REMOVE GET AND RUN FUNCTIONS'''
    def get(self):
        if self.mainwindow.winfo_exists():
           self.master.wait_window(self.mainwindow)
        return self.response

    def run(self):
        self.mainwindow.mainloop()
    ''' END OF MANDATORY METHODS '''

    def assing_to_existing(self):
        pass
    def assign_to_new(self):
        group_create = Groupcreate(self.mainwindow, self.eleana)
        response = group_create.get()
        print('Wykonano okienko')

    def cancel(self):
        self.mainwindow.destroy()
    # def ok_clicked(self):
    #     # Set the response to the text in the textbox and close the modal window
    #     self.response = self.text_box.get("1.0", "end-1c")  #
    #     self.mainwindow.destroy()
    #     pass

if __name__ == "__main__":
    app = Groupassign()
    app.run()

