#!/usr/bin/python3
import pathlib
import pygubu
import customtkinter
import copy
import matplotlib.pyplot as plt

from CTkColorPicker import AskColor
from CTkSpinbox import CTkSpinbox

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "preferences.ui"

class PreferencesApp:
    def __init__(self, app_instance):
        self.grapher = app_instance.grapher
        self.master = app_instance.mainwindow
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        self.matplotlib_styles = {
                                "default": "default",
                                "classic": "classic",
                                "solarize light": "Solarize_Light2",
                                "bmh": "bmh",
                                "dark background":"dark_background",
                                "fast": "fast",
                                "five thirty eight": "fivethirtyeight",
                                "ggplot": "ggplot",
                                "grayscale": "grayscale",
                                "seaborn bright": "seaborn-v0_8-bright",
                                "seaborn": "seaborn-v0_8",
                                "seaborn colorblind": "seaborn-v0_8-colorblind",
                                "seaborn dark": "seaborn-v0_8-dark",
                                "seaborn dark palette": "seaborn-v0_8-dark-palette",
                                "seaborn dark grid": "seaborn-v0_8-darkgrid",
                                "seaborn deep": "seaborn-v0_8-deep",
                                "seaborn muted": "seaborn-v0_8-muted",
                                "seaborn notebook": "seaborn-v0_8-notebook",
                                "seaborn paper": "seaborn-v0_8-paper",
                                "seaborn pastel": "seaborn-v0_8-pastel",
                                "seaborn poster": "seaborn-v0_8-poster",
                                "seaborn talk": "seaborn-v0_8-talk",
                                "seaborn ticks": "seaborn-v0_8-ticks",
                                "seaborn white": "seaborn-v0_8-white",
                                "seaborn whitegrid": "seaborn-v0_8-whitegrid",
                                "tableau colorblind": "tableau-colorblind10"
                                }

        # Main widget
        self.mainwindow = builder.get_object("toplevel1", self.master)
        builder.connect_callbacks(self)
        self.mainwindow.title('Preferences')
        self.mainwindow.attributes('-topmost', False)

        # References to settings
        self.style_first = self.grapher.style_first
        self.style_second = self.grapher.style_second
        self.style_result = self.grapher.style_result
        self.gui_appearence = app_instance.gui_appearence
        self.color_mode = app_instance.color_theme
        self.plt_style = self.grapher.plt_style

        # Copy current settings
        self.copy_style_first = copy.copy(self.style_first)
        self.copy_style_second = copy.copy(self.style_second)
        self.copy_style_result = copy.copy(self.style_result)
        self.copy_plt_style = copy.copy(self.plt_style)
        self.copy_gui_appearence = copy.copy(self.gui_appearence)
        self.copy_color_mode = copy.copy(self.color_mode)

        # References to widgets
        self.gui_style_box = builder.get_object("gui_style_box", self.mainwindow)
        self.color_scheme_box = builder.get_object("color_scheme_box", self.mainwindow)
        self.graph_general_box = builder.get_object('graph_general_box', self.mainwindow)
        self.first_plot_type_box = builder.get_object('ctkcombobox1', self.mainwindow)
        self.first_linewidth = builder.get_object('spinbox1', self.mainwindow)
        self.first_linestyle = builder.get_object('ctkcombobox2', self.mainwindow)
        self.first_marker = builder.get_object('ctkcombobox3', self.mainwindow)
        self.first_markersize = builder.get_object('spinbox2', self.mainwindow)
        self.btn_first_color_re = builder.get_object('ctkbutton2', self.mainwindow)
        self.btn_first_color_im = builder.get_object('ctkbutton3', self.mainwindow)

        self.second_plot_type_box = builder.get_object('ctkcombobox7', self.mainwindow)
        self.second_linewidth = builder.get_object('spinbox5', self.mainwindow)
        self.second_linestyle = builder.get_object('ctkcombobox8', self.mainwindow)
        self.second_marker = builder.get_object('ctkcombobox9', self.mainwindow)
        self.second_markersize = builder.get_object('spinbox6', self.mainwindow)
        self.btn_second_color_re = builder.get_object('ctkbutton6', self.mainwindow)
        self.btn_second_color_im = builder.get_object('ctkbutton7', self.mainwindow)

        self.result_plot_type_box = builder.get_object('ctkcombobox10', self.mainwindow)
        self.result_linewidth = builder.get_object('spinbox7', self.mainwindow)
        self.result_linestyle = builder.get_object('ctkcombobox11', self.mainwindow)
        self.result_marker = builder.get_object('ctkcombobox12', self.mainwindow)
        self.result_markersize = builder.get_object('spinbox8', self.mainwindow)
        self.btn_result_color_re = builder.get_object('ctkbutton8', self.mainwindow)
        self.btn_result_color_im = builder.get_object('ctkbutton9', self.mainwindow)

        self.response = None
        self.on_start()

        # Set values for graph_general_box
        styles = tuple(self.matplotlib_styles.keys())
        self.graph_general_box.configure(values=styles)


        # Replace tkinter spinboxes with ctkspinbox
        self.ctkframe9 = builder.get_object("ctkframe9", self.mainwindow)
        self.first_linewidth.grid_remove()
        self.first_linewidth = CTkSpinbox(self.ctkframe9, command=self.selected_first_linewidth, min_value=1)
        self.first_linewidth.grid(column=1, row=0, sticky="ew", padx=0)

    ''' STANDARD METHODS TO HANDLE WINDOW BEHAVIOR '''
    def get(self):
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event=None):
        ''' Close the window without changes '''
        # Restore original data
        self.style_first = copy.copy(self.copy_style_first)
        self.style_second = copy.copy(self.copy_style_second)
        self.style_result = copy.copy(self.copy_style_result)
        self.plt_style = copy.copy(self.copy_plt_style)
        self.gui_appearence = copy.copy(self.copy_gui_appearence)
        self.color_mode = copy.copy(self.copy_color_mode)

        #Set response to None and close
        self.response = None
        self.mainwindow.destroy()

    def ok(self):
        self.response = {'gui_appearance':self.gui_appearence, 'color_theme':self.color_mode}
        self.mainwindow.destroy()
    def run(self):
        self.mainwindow.mainloop()
    ''' END OF STANDARD METHODS '''

    def on_start(self):
        '''
        This sets the values to the widgets according
        to what is set in the grapher preferences and GUI
        '''

        # Application style
        self.gui_style_box.set(self.gui_appearence)
        self.color_scheme_box.set(self.color_mode)
        self.graph_general_box.set(self.plt_style)

        self.first_plot_type_box.set(self.style_first['plot_type'])
        self.first_linewidth.delete(0,'end')
        self.first_linewidth.insert(0, self.style_first['linewidth'])
        self.first_linestyle.set(self.style_first['linestyle'])
        self.first_marker.set(self.style_first['marker'])
        self.first_markersize.delete(0, 'end')
        self.first_markersize.insert(0, self.style_first['s'])
        self.btn_first_color_re.configure(fg_color = self.style_first['color_re'])
        self.btn_first_color_im.configure(fg_color = self.style_first['color_im'])

        self.second_plot_type_box.set(self.style_second['plot_type'])
        self.second_linewidth.delete(0, 'end')
        self.second_linewidth.insert(0, self.style_second['linewidth'])
        self.second_linestyle.set(self.style_second['linestyle'])
        self.second_marker.set(self.style_second['marker'])
        self.second_markersize.delete(0, 'end')
        self.second_markersize.insert(0, self.style_second['s'])
        self.btn_second_color_re.configure(fg_color=self.style_second['color_re'])
        self.btn_second_color_im.configure(fg_color=self.style_second['color_im'])

        self.result_plot_type_box.set(self.style_result['plot_type'])
        self.result_linewidth.delete(0, 'end')
        self.result_linewidth.insert(0, self.style_result['linewidth'])
        self.result_linestyle.set(self.style_result['linestyle'])
        self.result_marker.set(self.style_result['marker'])
        self.result_markersize.delete(0, 'end')
        self.result_markersize.insert(0, self.style_result['s'])
        self.btn_result_color_re.configure(fg_color=self.style_result['color_re'])
        self.btn_result_color_im.configure(fg_color=self.style_result['color_im'])

    def select_gui_appearance(self, value):
        self.gui_appearence = value
        customtkinter.set_appearance_mode(self.gui_appearence)

    def select_color_scheme(self, value):
        self.color_mode = value
        customtkinter.set_default_color_theme(self.color_mode)


    # Set plot style for First
    def selected_first_plot_type(self, value):
        self.style_first['plot_type'] = value.lower()
        self.grapher.plot_graph()

    def selected_first_linewidth(self):
        linewidth = int(self.first_linewidth.get())
        self.style_first['linewidth'] = linewidth
        self.grapher.plot_graph()

    def selected_first_linestyle(self, value):
        self.style_first['linestyle'] = value
        self.grapher.plot_graph()

    def selected_first_marker(self, value):
        self.style_first['marker'] = value
        self.grapher.plot_graph()

    def selected_first_markersize(self):
        s = int(self.first_markersize.get())
        self.style_first['s'] = s
        self.grapher.plot_graph()

    # Handle button of color selection
    def select_first_re(self):
        color = self.select_color()
        if not color:
            return
        self.btn_first_color_re.configure(fg_color = color)
        self.style_first['color_re'] = color
        self.grapher.plot_graph()

    def select_first_im(self):
        color = self.select_color()
        if not color:
            return
        self.btn_first_color_im.configure(fg_color = color)
        self.style_first['color_im'] = color
        self.grapher.plot_graph()

    # Set plot style for Second
    def selected_second_plot_type(self, value):
        self.style_second['plot_type'] = value.lower()
        self.grapher.plot_graph()

    def selected_second_linewidth(self):
        linewidth = int(self.second_linewidth.get())
        self.style_second['linewidth'] = linewidth
        self.grapher.plot_graph()

    def selected_second_linestyle(self, value):
        self.style_second['linestyle'] = value
        self.grapher.plot_graph()

    def selected_second_marker(self, value):
        self.style_second['marker'] = value
        self.grapher.plot_graph()

    def selected_second_markersize(self):
        s = int(self.second_markersize.get())
        self.style_second['s'] = s
        self.grapher.plot_graph()

    def select_second_re(self):
        color = self.select_color()
        if not color:
            return
        self.btn_second_color_re.configure(fg_color = color)
        self.style_second['color_re'] = color
        self.grapher.plot_graph()

    def select_second_im(self):
        color = self.select_color()
        if not color:
            return
        self.btn_second_color_im.configure(fg_color = color)
        self.style_second['color_im'] = color
        self.grapher.plot_graph()

    # Set plot style for Result
    def selected_result_plot_type(self, value):
        self.style_result['plot_type'] = value.lower()
        self.grapher.plot_graph()
    def selected_result_linewidth(self):
        linewidth = int(self.result_linewidth.get())
        self.style_result['linewidth'] = linewidth
        self.grapher.plot_graph()

    def selected_result_linestyle(self, value):
        self.style_result['linestyle'] = value
        self.grapher.plot_graph()

    def selected_result_marker(self, value):
        self.style_result['marker'] = value
        self.grapher.plot_graph()

    def selected_result_markersize(self):
        s = int(self.result_markersize.get())
        self.style_result['s'] = s
        self.grapher.plot_graph()

    def select_result_re(self):
        color = self.select_color()
        if not color:
            return
        self.btn_result_color_re.configure(fg_color = color)
        self.style_result['color_re'] = color
        self.grapher.plot_graph()

    def select_result_im(self):
        color = self.select_color()
        if not color:
            return
        self.btn_result_color_im.configure(fg_color = color)
        self.style_result['color_im'] = color
        self.grapher.plot_graph()

    def select_color(self):
        """
        Opens the dialog window of color picker
        """
        self.mainwindow.attributes('-topmost', False)
        ask_color = AskColor(self.mainwindow)
        selected_color = ask_color.get()
        self.mainwindow.attributes('-topmost', True)
        return selected_color

    def appearence(self, value):
        style = self.matplotlib_styles[value]
        if style:
            self.grapher.update_plot_style(style)
        else:
            print(value)
        return



if __name__ == "__main__":
    app = PreferencesApp()
    app.run()

