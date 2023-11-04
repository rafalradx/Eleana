#!/usr/bin/python3
import pathlib
import pygubu
from subprogs.group_edit.add_group import Groupcreate
from assets.DataClasses import Single2D
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "stack_to_group.ui"
import numpy as np

class StackToGroup:
    def __init__(self, master=None, eleana_instance=None, which='first'):
        self.eleana = eleana_instance
        self.builder = builder = pygubu.Builder()
        self.master = master.mainwindow
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", self.master)
        builder.connect_callbacks(self)

        # Set the window properties to modal mode
        self.mainwindow.grab_set()  # Set as modal
        self.mainwindow.attributes('-topmost', True)  # Always on top
        self.mainwindow.title('Convert 2D stack to group')

        self.btn_to_existing = builder.get_object("btn_to_existing", self.mainwindow)
        self.btn_new = builder.get_object("btn_new", self.mainwindow)
        self.btn_cancel = builder.get_object("btn_cancel", self.mainwindow)
        self.sel_group = builder.get_object("sel_group", self.mainwindow)
        self.name_label = builder.get_object('ctklabel1', self.mainwindow)
        self.which = which

        self.index = self.eleana.selections[self.which]

        asToGr = self.eleana.assignmentToGroups
        del asToGr['<group-list/>']
        groups = list(asToGr.keys())
        self.sel_group.configure(values=groups)
        self.sel_group.set('All')
        self.mainwindow.bind("<Escape>", self.quit)
        self.display_data_groups()

        self.response = None
    def get(self):
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def run(self):
        self.display_data_groups()
        self.mainwindow.mainloop()

    ''' END OF MANDATORY METHODS '''
    def quit(self, event = None):
        self.mainwindow.destroy()
    def assign_to_existing(self):
        group = self.sel_group.get()
        self.unfold_stack(group)
        pass
    def assign_to_new(self):
        group_create = Groupcreate(self.mainwindow, self.eleana)
        new_group = group_create.get()
        self.unfold_stack(new_group)
        pass

    def unfold_stack(self, group):
        dt = self.eleana.dataset[self.index]
        group = [group]
        stk_names = dt.stk_names
        name = dt.name
        data = {'parameters':   dt.parameters,
                'groups':       group,
                'x':            dt.x,
                'y':            np.array([]),
                'name':         name,
                'complex':      dt.complex,
                'type':         'single 2D',
                'origin':       dt.origin,
                }
        i = 0
        for stk in stk_names:
            data['name'] = name + '/' + stk
            data['y'] = dt.y[i]
            new_data = Single2D(data)
            self.eleana.dataset.append(new_data)
            i += 1
            self.response = group
            self.quit()

    def display_data_groups(self):
        data_name = self.eleana.dataset[self.index].name_nr
        groups = self.eleana.dataset[self.index].groups
        if len(groups) == 0:
            groups = ['All']
        self.eleana.dataset[self.index].groups = groups
        text = "NAME: " + data_name
        self.name_label.configure(text=text)


if __name__ == "__main__":
    app = StackToGroupApp()
    app.run()
