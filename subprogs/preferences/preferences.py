#!/usr/bin/python3
import pathlib
import pygubu
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "preferences.ui"


class PreferencesApp:
    def __init__(self, master=None, preferences={}):
        self.master = master
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", self.master)
        builder.connect_callbacks(self)
        self.mainwindow.title('Preferences')

        # References to widgets
        self.gui_style_box = builder.get_object("gui_style_box", self.mainwindow)
        self.color_scheme_box = builder.get_object("color_scheme_box", self.mainwindow)
        self.graph_general_box = builder.get_object('graph_general_box', self.mainwindow)
        self.first_plot_type_box = builder.get_object('first_plot_type_box', self.mainwindow)
        self.first_linewidth = builder.get_object('first_linewidth', self.mainwindow)
        self.first_linestyle = builder.get_object('first_linestyle', self.mainwindow)
        self.first_marker = builder.get_object('first_marker', self.mainwindow)
        self.first_markersize = builder.get_object('first_markersize', self.mainwindow)
        self.btn_first_color_re = builder.get_object('btn_first_color_re', self.mainwindow)



        self.response = None;
        # preferences contains list of settings to control
        self.preferences = preferences

        self.on_start()
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

    def on_start(self):
        # Application style
        style = self.preferences.get('gui_style', 'light')
        self.gui_style_box.set(style)
        color_scheme = self.preferences.get('gui_style', 'green')
        self.color_scheme_box.set(color_scheme)

        # Graph Styles
        graph_style = self.preferences.get('plt_style', 'default')
        self.graph_general_box.set(graph_style)

        # Styles for First

    def appearence(self, value):
        pass


if __name__ == "__main__":
    app = PreferencesApp()
    app.run()

