#!/usr/bin/python3
import pathlib
import pygubu
PROJECT_PATH = pathlib.Path(__file__).parent

# Adjust the name of the file with UI
PROJECT_UI = PROJECT_PATH / "add_group.ui"


class Groupeditor:
    def __init__(self, eleana_instance = None, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)
        # Reference to master window and eleana instance and response variable
        self.master = master
        self.eleana = eleana_instance
        self.response = None
        ''' Do not modify the code until this part'''


        # Set the window properties to modal mode
        self.mainwindow.grab_set()  # Set as modal
        self.mainwindow.attributes('-topmost', True)  # Always on top
        self.mainwindow.title('Add new group')
        #self.mainwindow.geometry('300x300')

        # Define references to objects in the window
        # --- example: self.text_box contains textbox widget object
        self.group_name = builder.get_object("ctkentry2", self.mainwindow)
        self.description = builder.get_object("ctkentry3", self.mainwindow)

    ''' DO NOT REMOVE GET AND RUN FUNCTIONS'''
    def get(self):
        if self.mainwindow.winfo_exists():
           self.master.wait_window(self.mainwindow)
        return self.response

    def run(self):
        self.mainwindow.mainloop()
    ''' END OF MANDATORY METHODS '''

    def create_group(self):
        groups = []

        groups = self.eleana.assignmentToGroups.keys()
        print(groups)
        print(self.group_name.get())

    def cancel(self):
        self.mainwindow.destroy()
    # def ok_clicked(self):
    #     # Set the response to the text in the textbox and close the modal window
    #     self.response = self.text_box.get("1.0", "end-1c")  #
    #     self.mainwindow.destroy()
    #     pass

if __name__ == "__main__":
    app = Groupeditor()
    app.run()

