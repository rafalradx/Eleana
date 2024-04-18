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
        self.btn_first_color_im = builder.get_object('btn_first_color_im', self.mainwindow)

        self.second_plot_type_box = builder.get_object('ctkcombobox4', self.mainwindow)
        self.second_linewidth = builder.get_object('spinbox11', self.mainwindow)
        self.second_linestyle = builder.get_object('ctkcombobox28', self.mainwindow)
        self.second_marker = builder.get_object('ctkcombobox29', self.mainwindow)
        self.second_markersize = builder.get_object('spinbox12', self.mainwindow)
        self.btn_second_color_re = builder.get_object('ctkbutton9', self.mainwindow)
        self.btn_second_color_im = builder.get_object('ctkbutton10', self.mainwindow)

        self.result_plot_type_box = builder.get_object('ctkcombobox33', self.mainwindow)
        self.result_linewidth = builder.get_object('spinbox15', self.mainwindow)
        self.result_linestyle = builder.get_object('ctkcombobox34', self.mainwindow)
        self.result_marker = builder.get_object('ctkcombobox35', self.mainwindow)
        self.result_markersize = builder.get_object('spinbox16', self.mainwindow)
        self.btn_result_color_re = builder.get_object('ctkbutton13', self.mainwindow)
        self.btn_result_color_im = builder.get_object('ctkbutton14', self.mainwindow)

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

        # First, Second and Result
        pref_first = self.preferences.get('pref_first', None)
        pref_second = self.preferences.get('pref_second', None)
        pref_result = self.preferences.get('pref_result', None)

        if not pref_first:
            print('First preferences not available.')
            pref_first = {'plot_type': 'line',
                            'linewidth': 3,
                            'linestyle':'solid',
                            'marker': '.',
                            's': 5,
                            'color_re': "#d53339",
                            'color_im': "#ef6f74"
                            }
        if not pref_second:
            print('Second preferences not available.')
            pref_second = {'plot_type': 'line',
                             'linewidth': 3,
                             'linestyle': 'solid',
                             's': 5,
                             'marker':'.',
                             'color_re': '#008cb3',
                             'color_im': '#07bbed'
                             }
        if not pref_result:
            print('Result preferences not available.')
            pref_result = {'plot_type': 'line',
                             'linewidth': 3,
                             'linestyle': 'solid',
                             's': 5,
                             'marker': '.',
                             'color_re': '#108d3d',
                             'color_im': '#32ab5d'
                             }
        self.first_plot_type_box.set(pref_first['plot_type'].title())
        self.first_linewidth.delete(0,'end')
        self.first_linewidth.insert(0, pref_first['linewidth'])
        self.first_linestyle.set(pref_first['linestyle'])
        self.first_marker.set(pref_first['marker'])
        self.first_markersize.delete(0, 'end')
        self.first_markersize.insert(0, pref_first['s'])
        self.btn_first_color_re.configure(fg_color = pref_first['color_re'])
        self.btn_first_color_im.configure(fg_color = pref_first['color_im'])

        self.second_plot_type_box.set(pref_second['plot_type'].title())
        self.second_linewidth.delete(0, 'end')
        self.second_linewidth.insert(0, pref_second['linewidth'])
        self.second_linestyle.set(pref_second['linestyle'])
        self.second_marker.set(pref_second['marker'])
        self.second_markersize.delete(0, 'end')
        self.second_markersize.insert(0, pref_second['s'])
        self.btn_second_color_re.configure(fg_color=pref_second['color_re'])
        self.btn_second_color_im.configure(fg_color=pref_second['color_im'])

        self.result_plot_type_box.set(pref_result['plot_type'].title())
        self.result_linewidth.delete(0, 'end')
        self.result_linewidth.insert(0, pref_result['linewidth'])
        self.result_linestyle.set(pref_result['linestyle'])
        self.result_marker.set(pref_result['marker'])
        self.result_markersize.delete(0, 'end')
        self.result_markersize.insert(0, pref_result['s'])
        self.btn_result_color_re.configure(fg_color=pref_result['color_re'])
        self.btn_result_color_im.configure(fg_color=pref_result['color_im'])

    def appearence(self, value):
        pass


if __name__ == "__main__":
    app = PreferencesApp()
    app.run()

