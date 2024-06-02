#!/usr/bin/python3
import pathlib
import pygubu
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from modules.CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
import copy
PROJECT_PATH = pathlib.Path(__file__).parent.parent
PROJECT_UI = PROJECT_PATH / "ui" / "StaticPlotWindow.ui"


class Staticplotwindow:
    def __init__(self, window_nr, static_plot_index, eleana_static_plots, eleana_active_static_plots, master):
        self.window_nr = window_nr
        self.plot_nr = static_plot_index
        self.static_plots = eleana_static_plots
        self.active_static_plots = eleana_active_static_plots
        matplotlib.use('TkAgg')
        self.plot_data = eleana_static_plots[self.plot_nr]
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel2", master)
        builder.connect_callbacks(self)
        self.mainwindow.title(self.plot_data['name'])

        # References to widgets
        self.graphFrame = builder.get_object('graphFrame', self.mainwindow)
        self.check_on_top = builder.get_object('check_on_top', self.mainwindow)
        self.leftFrame = builder.get_object('leftFrame', self.mainwindow)
        self.commentField = builder.get_object('commentField', self.mainwindow)

        # Create canvas
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphFrame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.canvas.draw()

        # Create toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graphFrame, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0, sticky="ew")

        # Configure grid resizing
        self.graphFrame.grid_rowconfigure(0, weight=1)
        self.graphFrame.grid_columnconfigure(0, weight=1)

        # Remove unused leftFrame:
        self.leftFrame.grid_remove()
        # Plot graph
        self.plot_graph()

        # Set controls according to plot_data
        on_top = self.plot_data.get("on_top", False)
        if on_top:
            self.check_on_top.select()
        else:
            self.check_on_top.deselect()

        # Call Cancel function when close window clicked
        self.mainwindow.protocol('WM_DELETE_WINDOW', self.cancel)

        comment = self.plot_data.get("comment", None)
        if comment:
            self.commentField.insert(0.0, comment)

    ''' DO NOT REMOVE GET AND RUN FUNCTIONS'''

    def get(self):
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event=None):
        self.response = None
        self.active_static_plots.remove(self.window_nr)
        self.mainwindow.destroy()

    def run(self):
        self.mainwindow.mainloop()

    ''' END OF MANDATORY METHODS '''

    def plot_graph(self):
        '''
        Add curves from self.plot_data to canvas
        '''
        def _getdata(curve_nr):
            curve = self.plot_data['curves'][curve_nr]
            disp = curve['disp']
            if not disp:
                return None, None, '', '', (), (), ()
            legend = curve['legend']
            style = curve['style']
            x = curve['x']
            re_y = curve['re_y']
            im_y = curve['im_y']
            type = curve['style']['plot_type']
            return disp, type, legend, style, x, re_y, im_y
        # Curve 0
        curve_nr = [0, 1, 2]
        for curve in curve_nr:
            disp, type, legend, style, x, re_y, im_y = _getdata(curve)
            if disp == 'cpl':
                if style['plot_type'] == 'line':
                    self.ax.plot(x, re_y, label=legend, color=style['color_re'], linewidth=style['linewidth'], linestyle=style['linestyle'])
                    self.ax.plot(x, im_y, label=legend, color=style['color_im'], linewidth=style['linewidth'], linestyle=style['linestyle'])
                else:
                    self.ax.scatter(x, re_y, label=legend, color=style['color_re'], s=style['s'], marker=style['marker'])
                    self.ax.scatter(x, im_y, label=legend, color=style['color_im'], s=style['s'], marker=style['marker'])
            elif disp == 'im':
                if style['plot_type'] == 'line':
                    self.ax.plot(x, im_y, label=legend, color=style['color_im'], linewidth=style['linewidth'], linestyle=style['linestyle'])
                else:
                    self.ax.scatter(x, im_y, label=legend, color=style['color_im'], s=style['s'], marker=style['marker'])
            elif disp == 're':
                if style['plot_type'] == 'line':
                    self.ax.plot(x, re_y, label=legend, color=style['color_re'], linewidth=style['linewidth'], linestyle=style['linestyle'])
                else:
                    self.ax.scatter(x, re_y, label=legend, color=style['color_re'], s=style['s'], marker=style['marker'])
        self.ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
                       fancybox=False, shadow=False, ncol=5)
        self.ax.set_xscale(self.plot_data['x_scale'])
        self.ax.set_yscale(self.plot_data['y_scale'])
        self.ax.set_xlim(self.plot_data['x_lim'])
        self.ax.set_ylim(self.plot_data['y_lim'])
        # self.ax.invert_xaxis(self.plot_data['inverted_x'])
        self.canvas.draw()
        on_top = self.static_plots[self.plot_nr].get('on_top', None)
        if not on_top:
            return
        elif on_top:
            self.check_on_top.select()
        else:
            self.check_on_top.deselect()
        self.switch_on_top()

    def switch_on_top(self):
        mode = bool(self.check_on_top.get())
        self.plot_data['on_top'] = mode
        self.mainwindow.attributes('-topmost', mode)

    def ok(self):
        mode = bool(self.check_on_top.get())
        self.plot_data['comment'] = self.commentField.get(0.0, "end")
        self.static_plots[self.plot_nr]['on_top'] = mode
        self.cancel()
    def delete(self):
        msg = CTkMessagebox(title="Delete", message="Do you want to delete this plot",
                            icon="question", option_1="Cancel", option_2="No", option_3="Yes")
        response = msg.get()
        if response == "Yes":
            del self.static_plots[self.plot_nr]
            self.cancel()

if __name__ == "__main__":
    app = Staticplotwindow()
    app.run()
