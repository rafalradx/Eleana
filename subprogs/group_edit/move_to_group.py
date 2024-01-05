#!/usr/bin/python3
import pathlib
import pygubu
import copy
from subprogs.group_edit.add_group import Groupcreate
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "move_to_group.ui"

class MoveToGroup:
    def __init__(self, master=None, app_instance = None):
        self.eleana = app_instance.eleana
        self.app = app_instance
        self.master = master

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

        self.mainwindow.grab_set()  # Set as modal
        self.mainwindow.attributes('-topmost', True)  # Always on top
        self.mainwindow.title('Move data to other group')

        self.response = None

        self.sel_group = builder.get_object('sel_group', master)

        self.assignment_to_groups_copy = copy.copy(self.eleana.assignmentToGroups.get('<group-list/>', ['All']))
        self.groups = self.eleana.assignmentToGroups['<group-list/>']
        self.update_group_list()
        self.mainwindow.protocol('WM_DELETE_WINDOW', self.cancel)

    ''' DO NOT REMOVE GET AND RUN FUNCTIONS'''

    def get(self):
        ''' This function returns the output from the closed window'''
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def run(self):
        self.mainwindow.mainloop()

    def ok(self):
        self.response = self.sel_group.get()
        self.mainwindow.destroy()
        pass

    def create_new(self):
        group_create = Groupcreate(self.master, self.eleana)
        new_group = group_create.get()
        if not new_group or new_group in self.sel_group._values:
            return
        self.groups.append(new_group)
        self.update_group_list(new_group)

    def cancel(self):
        self.eleana.assignmentToGroups['<group-list/>'] = self.assignment_to_groups_copy
        self.response = None
        self.mainwindow.destroy()

    def update_group_list(self, selection = 'All'):
        self.sel_group.configure(values=self.groups)
        self.sel_group.set(selection)

if __name__ == "__main__":
    app = MoveToGroup()
    app.run()
