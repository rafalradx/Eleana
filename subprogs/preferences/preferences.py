#!/usr/bin/python3
import pathlib
import pygubu
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "preferences.ui"


class PreferencesApp:
    def __init__(self, master=None):
        self.master = master
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", self.master)
        builder.connect_callbacks(self)

        self.response = None;
    ''' STANDARD METHODS TO HANDLE WINDOW BEHAVIOR '''
    def get(self):
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event=None):
        # Close the application
        self.response = None

    def run(self):
        self.mainwindow.mainloop()

    ''' END OF STANDARD METHODS '''

    def appearence(self, value):
        pass


if __name__ == "__main__":
    app = PreferencesApp()
    app.run()

