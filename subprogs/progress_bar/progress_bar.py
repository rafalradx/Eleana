#!/usr/bin/python3
import pathlib
import pygubu
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "progress_bar.ui"


class ProgressBar:
    def __init__(self, master=None, title = None, label = None, maximum = 10):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # Window setup
        if title:
            self.mainwindow.title(title)
        else:
            self.mainwindow.title('Processing ...')


        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def stop_processing(self):
        pass


if __name__ == "__main__":
    app = ProgressBar()
    app.run()
