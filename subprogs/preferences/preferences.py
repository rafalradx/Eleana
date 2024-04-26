#!/usr/bin/python3
import pathlib
import pygubu
import customtkinter
import copy

from modules.CTkColorPicker import AskColor

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "preferences.ui"

class PreferencesApp:
    def __init__(self, master, grapher, color_theme):

        self.grapher = grapher
        self.master = master
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", self.master)
        builder.connect_callbacks(self)
        self.mainwindow.title('Preferences')
        self.mainwindow.attributes('-topmost', False)

        # References to settings
        self.style_first = grapher.style_first
        self.style_second = grapher.style_second
        self.style_result = grapher.style_result
        self.gui_appearence = customtkinter.get_appearance_mode()
        self.color_mode = color_theme
        self.plt_style = grapher.plt_style

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
        self.btn_first_color_im = builder.get_object('ctkbutton2', self.mainwindow)

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
        self.gui_apperance = copy.copy(self.copy_gui_appearence)
        self.color_mode = copy.copy(self.copy_color_mode)

        #Set response to None and close
        self.response = None
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

    # Handle button of color selection
    def select_first_re(self):
        color = self.select_color()
        if not color:
            return
        self.btn_first_color_re.configure(fg_color = color)
        self.style_first['color_re']
        self.grapher.draw()

    def select_first_im(self):
        color = self.select_color()
        if not color:
            return
        self.btn_first_color_im.configure(fg_color = color)
        self.style_first['color_im']
        self.grapher.draw()

    def select_second_re(self):
        color = self.select_color()
        if not color:
            return
        self.btn_first_color_re.configure(fg_color = color)
        self.style_second['color_re']
        self.grapher.draw()

    def select_second_im(self):
        color = self.select_color()
        if not color:
            return
        self.btn_second_color_im.configure(fg_color = color)
        self.style_second['color_im']
        self.grapher.draw()

    def select_result_re(self):
        color = self.select_color()
        if not color:
            return
        self.btn_result_color_re.configure(fg_color = color)
        self.style_result['color_re']
        self.grapher.draw()

    def select_result_im(self):
        color = self.select_color()
        if not color:
            return
        self.btn_result_color_im.configure(fg_color = color)
        self.style_result['color_im']
        self.grapher.draw()




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
        pass


if __name__ == "__main__":
    app = PreferencesApp()
    app.run()

