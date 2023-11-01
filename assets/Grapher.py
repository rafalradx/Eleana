
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
        #self.toolbar.configure(bg="#FDF6E3", background="#FDF6E3")


        ''' PLOT PREFERENCES '''
        # Autoscaling variables
        self.autoscaling = {'x': True, 'y': True}
        self.scale1 = {'x': [], 'y': []}

        # Plot styling
        self.colors = {'first_re':  "#d53339",
                      'first_im':   "#ef6f74",
                      'second_re':  "#008cb3",
                      'second_im':  "#07bbed",
                      'result_re':  "#108d3d",
                      'result_im':  "#32ab5d"
                      }
        # Logarythmic scales
        self.log_scales = {'x':False, 'y':False}

        # Show X as points
        self.indexed_x = False

    def axis_title(self, which=None):
        '''Creates title for y and x axes  from "which" dataset '''

        if which == None:
            axis_title = {'x_title': "Abscissa [a.u.]", 'y_title': "Ordinate [a.u.]"}
            return axis_title
        if which == 'first':
            display = self.eleana.selections['f_dsp']
        elif which == 'second':
            display = self.eleana.selections['s_dsp']
        elif which == 'result':
            display = self.eleana.selections['r_dsp']
        else:
            display = True

        if not display:
            axis_title = {'x_title': "Abscissa [a.u.]", 'y_title': "Ordinate [a.u.]"}
            return axis_title

        try:
            index = self.eleana.selections[which]
            data = self.eleana.dataset[index]
        except IndexError:
            return {'x_title': "Abscissa [a.u.]", 'y_title': "Ordinate [a.u.]"}

        name_x = data.parameters['name_x']
        unit_x = data.parameters['unit_x']
        name_y = data.parameters['name_y']
        try:
            unit_y = data.parameters['unit_y']
        except KeyError:
            unit_y = 'a.u.'
        if len(unit_x) == 0:
            unit_x = 'a.u.'
        if len(unit_y) == 0:
            unit_y = 'a.u.'
        title_x = name_x + ' [' + unit_x + ']'
        title_y = name_y + ' [' + unit_y + ']'
        axis_title = {'x_title':title_x, 'y_title': title_y}
        return axis_title

    def create_legend(self, which=None):
        ''' This method create legend for plot defined in "which" '''

        # 1. If which is selected to None then legend = "no plot" and return
        if which == None:
            legend = ''
            return legend

        # Get selected data from dataset and store in "data"
        try:
            index = self.eleana.selections[which]
            data = self.eleana.dataset[index]
        except IndexError:
            legend = ''
            return legend
        if index < 0:
            legend = ''
            return legend
        # 2. Chcek if "Show Checkbox" is True. If not then legend = "no plot" and return
        if which == 'first':
            display = self.eleana.selections['f_dsp']
        elif which == 'second':
            display = self.eleana.selections['s_dsp']
        elif which == 'result':
            display = self.eleana.selections['r_dsp']
        else:
            display = True
        if not display:
            legend = ''
            return legend

        # 3. Check if data is a stack 2D. If yes add appropriate stk name to the legend.
        name_stk = ''
        if data.type == 'stack 2D':
            if which == 'first':
                stk_index = self.eleana.selections['f_stk']
                name_stk = '/' + str(data.stk_names[stk_index])
            elif which == 'second':
                stk_index = self.eleana.selections['s_stk']
                name_stk = '/' + str(data.stk_names[stk_index])
            elif which == 'result':
                stk_index =  self.eleana.selections['r_stk']
                name_stk = '/' + str(data.stk_names[stk_index])
        legend = str(data.name_nr + name_stk)

        # 4. Check if data is complex then add RE, IM, CPL or MAGN to the legend
        if data.complex:
            if which == 'first':
                cplx = self.eleana.selections['f_cpl']
            elif which == 'second':
                cplx = self.eleana.selections['s_cpl']
            elif which == 'result':
                cplx = self.eleana.selections['r_cpl']
            else:
                cplx = ''
            legend = legend + ':' + cplx.upper()
        return legend

    def data_for_plot(self, which):
        ''' This methods gets data from 'first' or 'second' or 'result' and returns data for plot'''
        if which == 'first' and self.eleana.selections['f_dsp'] and self.eleana.selections['first'] >= 0:
            data = self.eleana.getDataFromSelection('first')
        elif which == 'second' and self.eleana.selections['s_dsp'] and self.eleana.selections['second'] >= 0:
            data = self.eleana.getDataFromSelection('second')
        elif which == 'result' and self.eleana.selections['r_dsp'] and self.eleana.selections['result'] >= 0:
            data = self.eleana.getDataFromSelection('result')
        else:
            data = {'x': [], 're_y': [], 'im_y': [], 'complex': False}
        return data

    def plot_graph(self):
        ''' This method plots the basic working plot with First,Second,Result'''
        self.ax.clear()

        # Add first
        data = self.data_for_plot('first')
        # If indexed is True replace X values with consecutive points
        if self.indexed_x:
            length = len(data['x'])+1
            data['x'] = [i for i in range(1, length)]
        first_shown = True if len(data['x']) > 0 else False
        legend = self.create_legend('first')
        if not first_shown:
            axis_title = {'x_title':'Abscissa [a.u.]', 'y_title': 'Ordinate [a.u.]'}
        else:
            axis_title = self.axis_title('first')
        if data['complex'] and self.eleana.selections['f_cpl'] == 'cpl':
            self.ax.plot(data['x'], data['re_y'], label=legend, color=self.colors['first_re'])
            self.ax.plot(data['x'], data['im_y'], label=legend, color=self.colors['first_im'] )
        elif data['complex'] and self.eleana.selections['f_cpl'] == 'im':
            self.ax.plot(data['x'], data['im_y'], label=legend, color=self.colors['first_im'])
        else:
            self.ax.plot(data['x'], data['re_y'], label=legend, color=self.colors['first_re'])
        self.ax.set_xlabel(axis_title['x_title'])
        self.ax.set_ylabel(axis_title['y_title'])

        # Add second
        data = self.data_for_plot('second')
        # If indexed is True replace X values with consecutive points
        if self.indexed_x:
            length = len(data['x']) + 1
            data['x'] = [i for i in range(1, length)]
        legend = self.create_legend('second')
        second_shown = True if len(data['x']) > 0 else False
        if second_shown and not first_shown:
            axis_title = self.axis_title('second')
        else:
            pass

        if data['complex'] and self.eleana.selections['s_cpl'] == 'cpl':
            self.ax.plot(data['x'], data['re_y'], label=legend, color=self.colors['second_re'])
            self.ax.plot(data['x'], data['im_y'], label=legend, color=self.colors['second_im'])
        elif data['complex'] and self.eleana.selections['s_cpl'] == 'im':
            self.ax.plot(data['x'], data['im_y'], label=legend, color=self.colors['second_im'])
        else:
            #self.ax2.cla()
            #self.ax2.plot(data['x'], data['re_y'], label=legend, color=self.colors['second_re'])
            self.ax.plot(data['x'], data['re_y'], label=legend, color=self.colors['second_re'])
        self.ax.set_xlabel(axis_title['x_title'])
        self.ax.set_ylabel(axis_title['y_title'])

        # Add result
        data = self.data_for_plot('result')
        # If indexed is True replace X values with consecutive points
        if self.indexed_x:
            length = len(data['x']) + 1
            data['x'] = [i for i in range(1, length)]
        legend = self.create_legend('result')
        result_shown = True if len(data['x']) > 0 else False
        if result_shown and not first_shown and not second_shown:
            axis_title = self.axis_title('result')
        else:
            pass

        if data['complex'] and self.eleana.selections['r_cpl'] == 'cpl':
            self.ax.plot(data['x'], data['re_y'], label=legend, color=self.colors['result_re'])
            self.ax.plot(data['x'], data['im_y'], label=legend, color=self.colors['result_im'])
        else:
            self.ax.plot(data['x'], data['re_y'], label=legend, color=self.colors['result_re'])
        self.ax.set_xlabel(axis_title['x_title'])
        self.ax.set_ylabel(axis_title['y_title'])

        # Log or Linear scales
        if self.log_scales['x']:
            self.ax.set_xscale('log')
        else:
            self.ax.set_xscale('linear')
        if self.log_scales['y']:
            self.ax.set_yscale('log')
        else:
            self.ax.set_yscale('linear')


        # Draw Graph
        self.draw()


    def comparison_plot(self, selected_items, shifts={}):
        print(' W grapherze. ', selected_items)
        return


    def draw(self):
        self.ax.legend(loc='upper center', bbox_to_anchor=(0.15, 1.1),
                       fancybox=False, shadow=False, ncol=5)
        # Handle autoscaling
        if self.autoscaling['x']:
            self.scale1['x'] = self.ax.get_xlim()
        else:
            self.ax.set_xlim(self.scale1['x'])

        if self.autoscaling['y']:
            self.scale1['y'] = self.ax.get_ylim()
        else:
            self.ax.set_ylim(self.scale1['y'])
        self.canvas.draw()

        # Connect changes in scales due to ZOOM or MOVE
        self.ax.callbacks.connect('ylim_changed', self.on_ylim_changed)
        self.ax.callbacks.connect('xlim_changed', self.on_xlim_changed)

    def autoscale(self, autoscaling: dict):
        self.autoscaling = autoscaling
        return

    ''' Handling events on graph (key press or navigation toolbar use) '''
    def on_key_press_on_graph(self, event):
        key_press_handler(event, self.canvas, self.toolbar)
        self.canvas.mpl_connect("key_press_event", self.on_key_press_on_graph)

    def on_ylim_changed(self, axes):
        ylim = self.ax.get_ylim()
        self.scale1['y'] = ylim
        self.autoscaling['y'] = False
        self.app.check_autoscale_y.deselect()

    def on_xlim_changed(self, axes):
        xlim = self.ax.get_xlim()
        self.scale1['x'] = xlim
        self.autoscaling['x'] = False
        self.app.check_autoscale_x.deselect()

