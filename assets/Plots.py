#!/usr/bin/python3
import pathlib
import pygubu
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

PROJECT_PATH = pathlib.Path(__file__).parent.parent
PROJECT_UI = PROJECT_PATH / "ui" / "StaticPlotWindow.ui"


class Staticplotwindow:
    def __init__(self, master=None, plot_data = None):
        matplotlib.use('TkAgg')
        self.plot_data = plot_data
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel2", master)
        builder.connect_callbacks(self)
        self.mainwindow.title(self.plot_data['name'])

        # References to widgets
        self.graphFrame = builder.get_object('graphFrame', self.mainwindow)

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

        # Plot graph
        self.plot_graph()

    ''' DO NOT REMOVE GET AND RUN FUNCTIONS'''

    def get(self):
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def run(self):
        self.mainwindow.mainloop()

    ''' END OF MANDATORY METHODS '''

    def run(self):
        self.mainwindow.mainloop()

    def plot_graph(self):
        '''
        Add curves from self.plot_data to canvas
        '''
        def _getdata(curve_nr):
            curve = self.plot_data['curves'][0]
            disp = curve['disp']
            legend = curve['legend']
            style = curve['style']
            x = curve['x']
            re_y = curve['re_y']
            im_y = curve['im_y']
            type = curve['style']['plot_type']
            return disp, type, legend, style, x, re_y, im_y

        # Curve 1
        curve = 0
        disp, type, legend, style, x, re_y, im_y = _getdata(curve)
        if disp == 'cpl':
            pass




if __name__ == "__main__":
    app = Staticplotwindow()
    app.run()
