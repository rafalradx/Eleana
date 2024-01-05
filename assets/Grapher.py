
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
import mplcursors
from modules.CTkListbox import CTkListbox
matplotlib.use('TkAgg')

class GraphPreferences:
    def __init__(self, app_instance):
        self.app = app_instance

        ''' CURSOR DEFINITIONS '''
        # Create avaliable cursor modes: hov - enable hover,
        #                                a_txt - display text label,
        #                                annot - display selection on graph
        #                                multp - enable multiple annotations on graph
        #                                store - enable collecting the selected points
        self.cursor_modes = [
                        {'label': 'None', 'hov':False, 'a_txt':False, 'annot':False, 'multip':False, 'store': False},
                        {'label': 'Continuous read XY', 'hov':True, 'a_txt':True, 'annot':True, 'multip':False, 'store': False},
                        {'label': 'Selection of points with labels', 'hov': False, 'annot':True, 'a_txt':True, 'multip':True, 'store': True},
                        {'label': 'Selection of points', 'hov': False, 'annot':True, 'a_txt': False, 'multip':True, 'store': True},
                        {'label': 'Numbered selections', 'hov':False, 'annot':True, 'a_txt': True, 'multip':True, 'store': True, 'nr': True},
                        {'label': 'Free select'},
                        {'label': 'Crosshair', 'hov':True, 'a_txt':True, 'annot':True, 'multip':False, 'store': False}
                        ]

        self.current_cursor_mode = self.cursor_modes[0]

        # Plot colors
        self.colors = {'first_re': "#d53339",
                       'first_im': "#ef6f74",
                       'second_re': "#008cb3",
                       'second_im': "#07bbed",
                       'result_re': "#108d3d",
                       'result_im': "#32ab5d"
                       }

        # Set cursor modes
        self.set_cursor_modes()

        # Canvas style
        plt.style.use('Solarize_Light2')
        #plt.style.use('dark_background')

        # Scale settings
        self.inverted_x_axis = False
        # Plot colors
        self.colors = {'first_re': "#d53339",
                       'first_im': "#ef6f74",
                       'second_re': "#008cb3",
                       'second_im': "#07bbed",
                       'result_re': "#108d3d",
                       'result_im': "#32ab5d"
                       }

    def set_cursor_modes(self):
        ''' This function creates list of cursor
            modes in cursor combobox'''
        box_values = []
        for each in self.cursor_modes:
            box_values.append(each['label'])
        self.app.sel_cursor_mode.configure(values=box_values)
        self.app.sel_cursor_mode.set('None')


class Grapher(GraphPreferences):
    def __init__(self, app_instance, eleana_instance):
        # Initialize GraphPreferences
        super().__init__(app_instance)
        ''' Initialize app, eleana and graphs objects (fig, canvas, toolbar)'''
        self.app = app_instance
        self.eleana = eleana_instance
        self.plt = plt
        self.mplcursors = mplcursors
        self.cursor = None

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

        # Create empty list of created annotations
        self.cursor_annotations = []

        # Create variable for storing min-max
        self.scale1 = {'x': [], 'y': []}

    '''Methods for the Grapher class '''
    def clear_plot(self):
        self.ax.clear()
        self.canvas.draw()

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

        name_x = data.parameters.get('name_x', 'Abscissa')
        unit_x = data.parameters.get('unit_x', 'a.u.')
        name_y = data.parameters.get('name_y', 'Ordinate')
        unit_y = data.parameters.get('unit_y', 'a.u.')
        title_x = name_x + ' [' + unit_x + ']'
        title_y = name_y + ' [' + unit_y + ']'
        axis_title = {'x_title':title_x, 'y_title': title_y}
        return axis_title

    def create_legend(self, which=None):
        ''' This method create legend for plot defined in "which" '''
        # 1. If which is selected to None then legend = "no plot" and return
        if which == None:
            legend = ' '
            return legend

        # Get selected data from dataset and store in "data"
        try:
            index = self.eleana.selections[which]
            data = self.eleana.results_dataset[index] if which == 'result' else self.eleana.dataset[index]
        except IndexError:
            legend = ' '
            return legend
        if index < 0:
            legend = ' '
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
            legend = ' '
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
        if bool(self.app.check_indexed_x.get()):
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
        if bool(self.app.check_indexed_x.get()):
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

            self.ax.plot(data['x'], data['re_y'], label=legend, color=self.colors['second_re'])
        self.ax.set_xlabel(axis_title['x_title'])
        self.ax.set_ylabel(axis_title['y_title'])

        # Add result
        data = self.data_for_plot('result')
        # If indexed is True replace X values with consecutive points
        if bool(self.app.check_indexed_x.get()):
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
        if bool(self.app.check_log_x.get()):
            self.ax.set_xscale('log')
        else:
            self.ax.set_xscale('linear')
        if bool(self.app.check_log_y.get()):
            self.ax.set_yscale('log')
        else:
            self.ax.set_yscale('linear')

        # Draw Graph
        self.draw()
        # Create cursor
        self.cursor_on_off()

    def draw(self):
        ''' Puts the selected curves on the graph'''
        self.ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
                       fancybox=False, shadow=False, ncol=5)
        # Handle autoscaling
        if bool(self.app.check_autoscale_x.get()):
            self.scale1['x'] = self.ax.get_xlim()
        else:
            self.ax.set_xlim(self.scale1['x'])
        if bool(self.app.check_autoscale_y.get()):
            self.scale1['y'] = self.ax.get_ylim()
        else:
            self.ax.set_ylim(self.scale1['y'])

        if self.inverted_x_axis:
            self.ax.invert_xaxis()

        # Draw canvas
        self.canvas.draw()

        # Connect changes in scales due to ZOOM or MOVE
        self.ax.callbacks.connect('ylim_changed', self.on_ylim_changed)
        self.ax.callbacks.connect('xlim_changed', self.on_xlim_changed)

    '''**********************************
    *                                   *
    *       CURSORS AND ANNOTATIONS     *
    *                                   *
    **********************************'''
    def mplcursor_crosshair(self, sel):
        _mode = self.current_cursor_mode['label']
        if _mode == "Crosshair":
            x, y = sel.target
            #sel.annotation.set_text(f'x: {x:.2f}\ny1: {y:.2f}')
            sel.annotation.set_text('')
            # Remove previous crosshairs
            for extra in sel.extras:
                extra.remove()
            sel.extras.clear()

            # Create new crosshairs
            hline = self.ax.axhline(y, color='k', ls=':')
            vline = self.ax.axvline(x, color='k', ls=':')
            sel.extras.append(hline)
            sel.extras.append(vline)

            # Update position of both lines of crosshair
            sel.extras[0].set_ydata([y, y])
            sel.extras[1].set_xdata([x, x])

    def cursor_on_off(self):
        def _show_annotation_list(self):
            self.app.annotationsFrame.grid()
            self.annotationlist = CTkListbox(self.app.annotationsFrame, command=self.updateAnnotationList,
                                             multiple_selection=True, height=300)
            self.annotationlist.grid(column=0, row=0, sticky="nsew")

        self.free_move_binding_id = None
        self.click_binding_id = None
        crs_mode = self.current_cursor_mode['label']
        try:
            for sel in self.cursor.selections:
                    self.cursor.remove_selection(sel)
        except:
            pass

        index = self.app.sel_cursor_mode._values.index(crs_mode)
        self.current_cursor_mode = self.cursor_modes[index]

        if index == 0:
            # Switch off mplcursors
            self.app.btn_clear_cursors.grid_remove()
            if hasattr(self.cursor, "events"):
                self.cursor.events["add"].disconnect()
                self.cursor = None
            self.app.annotationsFrame.grid_remove()
        elif index > 0 and index < 5:
            # Switch on the mplcursors
            self.app.btn_clear_cursors.grid()
            _show_annotation_list(self)
            self.cursor = self.mplcursors.cursor(self.ax,
                                                 multiple=self.current_cursor_mode['multip'],
                                                 hover=self.current_cursor_mode['hov'])
            self.cursor.connect("add", self.annotation_create)
            self.cursor.connect("remove", self.annotation_removed)

        elif index == 5:
            # Free select
            self.app.btn_clear_cursors.grid()
            _show_annotation_list(self)
            # Switch on Free point selections

            self.click_binding_id = self.canvas.mpl_connect('button_press_event', self.on_click_in_plot)

        elif index == 6:
            # Crosshair
            _show_annotation_list(self)
            self.cursor = self.mplcursors.cursor(self.ax, multiple=False, hover=True)
            self.cursor.connect("add", self.mplcursor_crosshair)
            self.click_binding_id = self.canvas.mpl_connect('button_press_event', self.on_click_in_plot)

        else:
            if hasattr(self.cursor, "events"):
                # Switch off mplcursor
                self.cursor.events["add"].disconnect()
                self.cursor = None
            self.app.annotationsFrame.grid_remove()
            # Switch off free mouse events
            if self.free_move_binding_id is not None:
                self.plt.disconnect(self.free_move_binding_id)
            if self.click_binding_id is not None:
                self.canvas.mpl_disconnect(self.click_binding_id)

    def on_click_in_plot(self, event):
        """ Get coordinates from graph when Free Select is set in the combobox """
        # Check if Zoom is activated or not
        state = self.toolbar.mode
        if state == 'zoom rect' or state == 'pan/zoom':
            return
        if (event.inaxes is not None and (self.app.sel_cursor_mode.get() == 'Free select' or self.app.sel_cursor_mode.get() == 'Crosshair') and event.button == 1):
            # Create annotation when left mouse button is clicked
            x, y = event.xdata, event.ydata
            point_selected = (x,y)
            current_nr = 0
            if self.cursor_annotations:
                last_annotation = self.cursor_annotations[-1]
                current_nr = last_annotation.get('nr', 0) + 1
            my_annotation = {'type': None, 'curve': 'XY', 'index': 0, 'stk_index': -1, 'point': point_selected,
                             'nr': current_nr}
            self.cursor_annotations.append(my_annotation)
            self.updateAnnotationList(action='add')
            text = ' '
            self.ax.annotate(text, xy=point_selected, arrowprops={})
            self.canvas.draw()

        elif (event.inaxes is not None and self.app.sel_cursor_mode.get() == 'Free select' and event.button == 3):
            # Remove annotation when right mouse button is clicked
            x, y = event.xdata, event.ydata
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            x_span = abs(xlim[1]-xlim[0])
            y_span = abs(ylim[1]-ylim[0])

            tolerance = 0.05  # Tolerancja dla porównania współrzędnych
            for annotation in self.ax.texts:
                x_diff = abs(annotation.xy[0] - x)
                y_diff = abs(annotation.xy[1] - y)
                if x_diff < tolerance*x_span and y_diff < tolerance*y_span:
                    annotation.remove()
            self.canvas.draw()
        else:
            return

    def annotation_create(self, sel):
        ''' This creates annotations on the graph and add selected
            to the list in self.cursor_annotations '''
        curve = sel.artist.get_label()
        x = sel.target[0]
        y = sel.target[1]

        # Get curve index
        curve_type, index, stk_index = self.indexCurveForAnnot(curve)
        point = [x,y]
        current_nr = 0

        if self.cursor_annotations:
            last_annotation = self.cursor_annotations[-1]
            current_nr = last_annotation.get('nr', 0) + 1
        my_annotation = {'type': curve_type, 'curve':curve, 'index':index, 'stk_index':stk_index, 'point':point, 'nr': current_nr}
        if not self.current_cursor_mode['hov']:
            self.cursor_annotations.append(my_annotation)
        label = f'Point: x={x:.2f}, y={y:.2f}'
        if not self.current_cursor_mode['a_txt']:
            label = ''
        elif self.current_cursor_mode.get('nr', False):
            label = str(current_nr)
        sel.annotation.set_text(label)
        sel.annotation.set_visible(self.current_cursor_mode['annot'])
        self.updateAnnotationList(action ='add')

    def annotation_removed(self, event):
        ''' This deletes selected annotation from the graph
            and removes the respective point from the list in
            self.cursor_annotations. '''
        annotation = event.annotation
        x = annotation.xy[0]
        y = annotation.xy[1]
        point = [x,y]
        points = [d['point'] for d in self.cursor_annotations if 'point' in d]
        if point in points:
            index = points.index(point)
            self.cursor_annotations.pop(index)
            self.updateAnnotationList()

    def clear_all_annotations(self, skip=None):
        self.cursor_annotations = []
        try:
            self.clearAnnotationList()
        except:
            pass
        if skip:
            return
        else:
            value = self.app.sel_cursor_mode.get()
            self.app.sel_graph_cursor(value)
        return

    def clearAnnotationList(self):
        elements = self.annotationlist.size()
        i = 0
        while i < elements:
            self.annotationlist.delete(0)
            i += 1

    def updateAnnotationList(self, action=None):
        self.clearAnnotationList()
        list_of_annotations = []
        for each in self.cursor_annotations:
            nr = each['nr']
            curve = each['curve']
            point_x = each['point'][0]
            point_y = each['point'][1]
            if nr < 10:
                nr = '#0' + str(nr)
            else:
                nr = '#' + str(nr)
            entry = nr + ' | ' + str(curve) + ' (' + str(round(point_x,2)) + ', ' + str(round(point_y, 2)) + ')'
            list_of_annotations.append(entry)
        i = 0
        while i < len(list_of_annotations):
            self.annotationlist.insert(i, list_of_annotations[i])
            i += 1
    def indexCurveForAnnot(self, curve):
        if self.app.sel_cursor_mode.get() == "Free select":
            return
        # Search name in the main dataset
        if '/' in curve:
            curve = curve.split('/')
            curve = curve[0]
        elif ':' in curve:
            curve = curve.split(':')
            curve = curve[0]
        i = 0
        while i < len(self.eleana.dataset):
            name = self.eleana.dataset[i].name_nr
            if name == curve:
                index = i
                break
            i += 1
        else:
            # If not found in main dataset then look in results_dataset
            i = 0
            while i < len(self.eleana.results_dataset):
                name = self.eleana.dataset[i].name_nr
                if name == curve:
                    index = i
                    break
                i += 1
            else:
                return None
        stk_index = -1
        if index == self.eleana.selections['first']:
            curve_type = 'first'
            if self.eleana.dataset[index].type == 'stack 2D':
                stk_index = self.eleana.selections['f_stk']
        elif index == self.eleana.selections['second']:
            curve_type = 'second'
            if self.eleana.dataset[index].type == 'stack 2D':
                stk_index = self.eleana.selections['s_stk']
        elif index == self.eleana.selections['result']:
            curve_type = 'results'
            if self.eleana.dataset[index].type == 'stack 2D':
                stk_index = self.eleana.selections['r_stk']
        else:
            curve_type = 'none'
        return curve_type, index, stk_index

    '''******************************************l.ann
    *                                           *
    *              EVENTS ON GRAPH              *
    *   (key press or navigation toolbar use)   *
    *                                           *
    ******************************************'''
    def on_key_press_on_graph(self, event):
        key_press_handler(event, self.canvas, self.toolbar)
        self.canvas.mpl_connect("key_press_event", self.on_key_press_on_graph)

    def on_ylim_changed(self, axes):
        ylim = self.ax.get_ylim()
        self.scale1['y'] = ylim
        self.app.check_autoscale_y.deselect()

    def on_xlim_changed(self, axes):
        xlim = self.ax.get_xlim()
        self.scale1['x'] = xlim
        self.app.check_autoscale_x.deselect()

    def plot_comparison(self, indexes, vsep, hsep):
        self.ax.clear()
        i = 0
        for each in indexes:
            x = self.eleana.dataset[each].x
            x = x - hsep[i]
            y = self.eleana.dataset[each].y
            y = y - vsep[i]
            self.ax.plot(x, y)
            i +=1
        self.canvas.draw()
