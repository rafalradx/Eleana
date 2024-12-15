#!/usr/bin/python3
import pathlib
import copy
import pygubu
from tkinter import Event
from modules.CTkMessagebox import CTkMessagebox
from subprogs.group_edit.add_group import Groupcreate
PROJECT_PATH = pathlib.Path(__file__).parent

# Adjust the name of the file with UI
PROJECT_UI = PROJECT_PATH / "assign_to_group.ui"

class Groupassign:
    def __init__(self, master = None, which = 'first', window_title = "Add new group"):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.app = master
        self.master = self.app.mainwindow
        self.eleana = self.app.eleana
        self.response = None
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
        self.group_field = builder.get_object('group_field', self.mainwindow)
        self.which = which

        # Check if
        self.index = self.eleana.selections[self.which]

        asToGr = self.eleana.assignmentToGroups
        del asToGr['<group-list/>']
        groups = list(asToGr.keys())
        self.sel_group.configure(values = groups)
        self.sel_group.set('All')
        self.mainwindow.bind("<Escape>", self.cancel)
        self.display_data_groups()

    ''' DO NOT REMOVE GET AND RUN FUNCTIONS'''
    def get(self):
        if self.mainwindow.winfo_exists():
           self.master.wait_window(self.mainwindow)
        return self.response

    def run(self):
        self.display_data_groups('<init label text>')
        self.mainwindow.mainloop()
    ''' END OF MANDATORY METHODS '''

    def assign_to_existing(self):
        new_group = self.sel_group.get()
        self.write_assignment_to_data(new_group)

    def assign_to_new(self):
        self.mainwindow.grab_release()
        self.mainwindow.attributes('-topmost', False)
        group_create = Groupcreate(self.mainwindow, self.eleana)
        new_group = group_create.get()
        self.write_assignment_to_data(new_group)
        self.mainwindow.grab_set()
        self.mainwindow.attributes('-topmost', True)


    def cancel(self, event: Event = None):
        self.mainwindow.destroy()

    def write_assignment_to_data(self, new_group):
        index = self.eleana.selections[self.which]
        if self.which == 'result':
            groups = ['All']
        else:
            groups = self.eleana.dataset[index].groups
        if new_group in groups:
            info = "'" + str(self.eleana.dataset[index].name_nr) + "'" + ' already belongs to ' + new_group
            CTkMessagebox(title="", message=info)
            return
        if self.which != 'result':
            data = copy.deepcopy(self.eleana.dataset[index])
            current_groups = data.groups
            current_groups.append(new_group)
            self.eleana.dataset[index].groups = current_groups
            self.display_data_groups()
        else:
            field_content = self.group_field.get('0.0', 'end')
            field_content = field_content.replace("\n", " ")
            field_content = field_content.replace("\t", " ")
            current_groups = field_content.split(',')
            current_groups = [el.replace(" ", "").replace("\t", "").replace("\n", "") for el in current_groups]
            current_groups.append(new_group)
            text = ", ".join(current_groups)
            self.group_field.configure(state="normal")
            self.group_field.delete("0.0", "end")
            self.group_field.insert("0.0", text)
            self.group_field.configure(state="disabled")
        self.response = current_groups

    def display_data_groups(self):
        data_name = self.eleana.dataset[self.index].name_nr
        groups = self.eleana.dataset[self.index].groups
        if len(groups) == 0 or type(groups) == str:
            groups = ['All']
        self.eleana.dataset[self.index].groups = groups
        groups = ', '.join(list(self.eleana.dataset[self.index].groups))
        text = 'NAME: ' + data_name
        self.name_label.configure(text=text)
        self.group_field.configure(state="normal")
        self.group_field.delete("0.0", "end")
        self.group_field.insert("0.0",  groups)
        self.group_field.configure(state="disabled")

if __name__ == "__main__":
    app = Groupassign()
    app.run()

