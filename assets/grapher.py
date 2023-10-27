
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot
import numpy as np

class Grapher:
    def __init__(self, app_instance, eleana_instance):
        ''' Initialize app, eleana and graphs objects (fig, canvas, toolbar'''
        self.app = app_instance
        self.eleana = eleana_instance

        matplotlib.pyplot.style.use('Solarize_Light2')

        # Create canvas
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.app.graphFrame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.canvas.draw()

        # Create toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.app.graphFrame, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0, sticky="ew")


        self.colours = {'first_re':   "#d53339",
                      'first_im':   "#ef6f74",
                      'second_re:': "#008cb3",
                      'second_im':  "#07bbed",
                      'result_re':  "#108d3d",
                      'result_im':  "#32ab5d"
                      }


    def plot_graph(self):

        # Clear canvas


        self.draw()


    def plot_graph(self):
        ''' Plots the graph in self.canvas.
            This is the main method for plotting working plot for first, second, and result'''

        # Clear canvas
        self.ax.clear()

        color_first_re = "#d53339"
        color_first_im = "#ef6f74"
        color_second_re = "#008cb3"
        color_second_im = "#07bbed"
        color_result_re = "#108d3d"
        color_result_im = "#32ab5d"


        first_complex = False
        second_complex = False
        result_complex = False

        # FIRST
        index = self.eleana.selections['first']
        is_first_not_none = [True if index >= 0 else False]

        if self.eleana.selections['f_dsp'] and index >= 0:
            data_for_plot = self.eleana.getDataFromSelection('first')
            data_index = self.eleana.selections['first']
            first_x = data_for_plot['x']
            first_complex = data_for_plot['complex']
            first_re_y = data_for_plot['re_y']
            first_im_y = data_for_plot['im_y']
            first_legend_index = self.eleana.selections['first']
            first_legend = self.eleana.dataset[first_legend_index].name_nr

            # Label for x axis
            try:
                label_x_title = self.eleana.dataset[data_index].parameters['name_x']
            except:
                label_x_title = ''
            try:
                label_x_unit = self.eleana.dataset[data_index].parameters['unit_x']
            except:
                label_x_unit = 'a.u.'
            first_label_x = label_x_title + ' [' + label_x_unit + ']'

            # Labels for y axis
            try:
                label_y_title = self.eleana.dataset[data_index].parameters['name_y']
            except:
                label_y_title = ''
            try:
                label_y_unit = self.eleana.dataset[data_index].parameters['unit_y']
            except:
                label_y_unit = 'a.u.'
            first_label_y = label_y_title + ' [' + label_y_unit + ']'

        else:
            first_x = np.array([])
            first_re_y = np.array([])
            first_im_y = np.array([])
            first_legend = 'no plot'
            first_label_x = ''
            first_label_y = ''

        # Add FIRST to plot
        self.ax.set_ylabel(first_label_y)
        self.ax.set_xlabel(first_label_x)
        if first_complex:
            if self.eleana.selections['f_cpl'] == 'im':
                first_legend = first_legend + ' :IMAG'
                self.ax.plot(first_x, first_im_y, label=first_legend, color=color_first_im)
            elif self.eleana.selections['f_cpl'] == 'magn':
                first_legend = first_legend + ' :MAGN'
                self.ax.plot(first_x, first_re_y, label=first_legend, color=color_first_re)
            elif self.eleana.selections['f_cpl'] == 'cpl':
                first_legend_r = first_legend + ' :REAL'
                self.ax.plot(first_x, first_re_y, label=first_legend_r, color=color_first_re)
                first_legend_i = first_legend + ' :IMAG'
                self.ax.plot(first_x, first_im_y, label=first_legend_i, color=color_first_im)
            elif self.eleana.selections['f_cpl'] == 're':
                first_legend = first_legend + ' :REAL'
                self.ax.plot(first_x, first_re_y, label=first_legend, color=color_first_re)
        else:
            self.ax.plot(first_x, first_re_y, label=first_legend, color=color_first_re)

        # SECOND
        index = self.eleana.selections['second']
        is_second_not_none = [True if index >= 0 else False]
        if self.eleana.selections['s_dsp'] and index >= 0:
            data_for_plot = self.eleana.getDataFromSelection('second')
            data_index = self.eleana.selections['second']
            second_x = data_for_plot['x']
            second_re_y = data_for_plot['re_y']
            second_im_y = data_for_plot['im_y']
            second_legend_index = self.eleana.selections['second']
            second_legend = self.eleana.dataset[second_legend_index].name_nr

            # Label for x axis
            try:
                label_x_title = self.eleana.dataset[data_index].parameters['name_x']
            except:
                label_x_title = ''
            try:
                label_x_unit = self.eleana.dataset[data_index].parameters['unit_x']
            except:
                label_x_unit = 'a.u.'
            second_label_x = label_x_title + ' [' + label_x_unit + ']'

            # Labels for y axis
            try:
                label_y_title = self.eleana.dataset[data_index].parameters['name_y']
            except:
                label_y_title = ''
            try:
                label_y_unit = self.eleana.dataset[data_index].parameters['unit_y']
            except:
                label_y_unit = 'a.u.'
            second_label_y = label_y_title + ' [' + label_y_unit + ']'

        else:
            second_x = np.array([])
            second_re_y = np.array([])
            second_im_y = np.array([])
            second_legend = 'no plot'
            second_label_x = ''
            second_label_y = ''

        # Add SECOND to plot
        if self.eleana.selections['f_dsp'] and index >= 0:
            # If FIRST spectrum is on then do not change axes labels
            pass
        else:
            # If FIRST spectrum is off or set tu None then change labels to those from SECOND
            self.ax.set_ylabel(second_label_y)
            self.ax.set_xlabel(second_label_x)

        self.ax.plot(second_x, second_re_y, label=second_legend, color=color_second_re)

        # RESULT
        if len(self.eleana.results_dataset) != 0:
            index = self.eleana.selections['first']

            if index >= 0:
                is_result_not_none = True
            else:
                is_result_not_none = False

            if self.eleana.selections['s_dsp'] and is_result_not_none:
                data_for_plot = self.eleana.getDataFromSelection('result')
                data_index = self.eleana.selections['result']
                result_x = data_for_plot['x']
                result_re_y = data_for_plot['re_y']
                result_im_y = data_for_plot['im_y']
                result_legend_index = self.eleana.selections['result']
                result_legend = self.eleana.results_dataset[result_legend_index].name_nr

                # Label for x axis
                try:
                    label_x_title = self.eleana.results_dataset[data_index].parameters['name_x']
                except:
                    label_x_title = ''
                try:
                    label_x_unit = self.eleana.results_dataset[data_index].parameters['unit_x']
                except:
                    label_x_unit = 'a.u.'
                result_label_x = label_x_title + ' [' + label_x_unit + ']'

                # Labels for y axis
                try:
                    label_y_title = self.eleana.results_dataset[data_index].parameters['name_y']
                except:
                    label_y_title = ''
                try:
                    label_y_unit = self.eleana.results_dataset[data_index].parameters['unit_y']
                except:
                    label_y_unit = 'a.u.'
                result_label_y = label_y_title + ' [' + label_y_unit + ']'

            else:
                result_x = np.array([])
                result_re_y = np.array([])
                result_im_y = np.array([])
                result_legend = 'no plot'
                result_label_x = ''
                result_label_y = ''

            # Add SECOND to plot
            if self.eleana.selections['f_dsp'] and self.eleana.selections['s_dsp'] and is_first_not_none and is_second_not_none:
                pass
            else:
                # If FIRST spectrum is off or set tu None then change labels to those from SECOND
                self.ax.set_ylabel(result_label_y)
                self.ax.set_xlabel(result_label_x)

            self.ax.plot(result_x, result_re_y, label=result_legend, color=color_result_re)

        # Put data on Graph
        self.ax.legend(loc='upper center', bbox_to_anchor=(0.15, 1.1),
                  fancybox=False, shadow=False, ncol=5)

        self.canvas.draw()

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, self.canvas, self.toolbar)

        self.canvas.mpl_connect("key_press_event", on_key_press)
    def draw(self):
        self.ax.legend(loc='upper center', bbox_to_anchor=(0.15, 1.1),
                       fancybox=False, shadow=False, ncol=5)
        self.canvas.draw()
        def on_key_press_on_graph(event):
           key_press_handler(event, self.canvas, self.toolbar)
           self.canvas.mpl_connect("key_press_event", on_key_press_on_graph)