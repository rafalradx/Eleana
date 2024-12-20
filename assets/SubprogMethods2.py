

from assets.Observer import Observer
import copy
import numpy as np
from assets.Error import Error
from subprogs.table.table import CreateFromTable
import pandas


class SubMethods_02:
    def __init__(self, app=None, which='first', commandline=False):
        self.commandline = commandline
        self.process_group_show_error = True
        self.update_gui = True
        self.stk_index = 0
        self.data_for_calculations = []
        if app and not self.commandline:
            # Window start from Menu in GUI
            self.app = app
            self.mainwindow.protocol('WM_DELETE_WINDOW', self.cancel)
            self.master = self.app.mainwindow
            self.eleana = self.app.eleana
            self.grapher = self.app.grapher
            self.update = self.app.update
            self.mainwindow.title(self.subwindow_settings['title'])
            self.mainwindow.attributes('-topmost', self.subwindow_settings['on_top'])
            if self.subwindow_settings['data_label']:
                self.data_label = self.builder.get_object(self.subwindow_settings['data_label'], self.mainwindow)
            else:
                self.data_label = None
        else:
            # Instance created directly from subprog.
            self.app = None
            self.master = None
            self.grapher = None
        # Set to which selection 'First' or 'Second'
        self.which = which
        # If self.app is defined, configure window, observer and grapher
        if self.app:
            # Custom window configuration in parrent
            self.configure_window()
            # Create observer
            self.observer = Observer(self.eleana, self)
            self.eleana.notify_on = True
            # Set current position in Results Dataset
            cursor_type = self.subprog_cursor['type'].lower()
            if  cursor_type != 'none' or cursor_type != '':
                # Configure cursor
                self.subprog_cursor['previous'] = copy.copy(self.grapher.current_cursor_mode['label'])
                self.grapher.cursor_limit = self.subprog_cursor['limit']
                self.app.sel_cursor_mode.set(self.subprog_cursor['type'])
                self.app.sel_graph_cursor(self.subprog_cursor['type'])
                if not self.subprog_cursor['changing']:
                    # Disable cursor changing
                    self.app.sel_cursor_mode.configure(state="disabled")

    def get(self):
        ''' Returns self.response to the main application after close '''
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event=None):
        ''' Close the window without changes '''
        self.response = None
        # Return cursor selection to enabled
        self.app.sel_cursor_mode.configure(state="normal")
        self.app.sel_cursor_mode.set(self.subprog_cursor['previous'])
        self.app.sel_graph_cursor(self.subprog_cursor['previous'])
        # Unregister observer
        self.eleana.detach(self.observer)
        self.grapher.clear_selected_ranges()
        self.mainwindow.destroy()

    #
    #   GETTING THE DATA ACCORDING TO THE SELECTION
    #
    def get_data(self, variable=None, value=None):
        ''' Makes a copy of the selected data and stores it in self.original_data.
            You may perform calculations on self.original_data. '''
        if self.eleana.selections[self.which] >= 0: # If selection is not None
            index = self.eleana.selections[self.which]
            self.eleana.notify_on = False
            self.original_data1 = copy.deepcopy(self.eleana.dataset[index])
            self.original_data2 = None
        else:
            if self.app:
                Error.show(info='No first data selected', details='')
            return False
        if self.use_second:
            # --- TWO DATA ARE NEEDED ---
            index2 = self.eleana.selections['second']
            if self.eleana.selections['second'] == -1:
                if self.app:
                    Error.show(info='No second data selected', details='')
                self.original_data2 = None
                return False
            self.original_data2 = copy.deepcopy(self.eleana.dataset[index2])
        return True

    def data_changed(self, variable, value):
        ''' Activate get_data when selection changed.
            This is triggered by the Observer.   '''
        print(f'variable = {variable} value = {value}')
        if variable == "first" and value is None:
            self.app.mainwindow.configure(cursor="")
            self.grapher.canvas.get_tk_widget().config(cursor="")
        elif variable == 'f_stk' or variable == 's_stk':
            self.app.mainwindow.configure(cursor="")
            self.grapher.canvas.get_tk_widget().config(cursor="")
            return False
        elif variable == 'grapher_action' and value == 'range_start':
            self.app.mainwindow.configure(cursor="")
            self.grapher.canvas.get_tk_widget().config(cursor="")
            return False
        elif variable == 'grapher_action' and value == 'range_end':
            if self.trigger_when_range_complete is False:
                self.app.mainwindow.configure(cursor="")
                self.grapher.canvas.get_tk_widget().config(cursor="")
                return False
        elif variable == "grapher_action":
            return False
        elif variable == 'result':
            return False
        if self.subwindow_settings['auto_calculate']:
            self.ok_clicked()
        return True

    #
    # TRIGGERING CALCULATIONS
    #
    def perform_single_calculations(self):
        ''' Performs calculations for single data selected in First or Second
            This function checks if this is a single data of stack and if stack
            can be calculated as separate data or must be taken as whole.
            This function is triggered by Clicking "Calculate" or data change in GUI
        '''
        self.set_mouse_state("watch")
        is_2D = self.original_data1.y.ndim == 2
        # Check if data is stack 2D
        if self.original_data1.type.lower() == 'stack 2D' or is_2D:
            # This is stack 2D then check if stack is calculated as separate data
            if not self.stack_sep:
                status = self.prepare_stack_for_calc() # Prepare the whole stack for calculations
                return status
            else:
                status = self.prepare_for_stack_separate()
                return status
        elif self.original_data1.type.lower() == 'single 2D' or not is_2D:
                status = self.prepare_single_data()

                # W tym miejscu skończyłem



                return status
        else:
            Error.show(info='The type of the selected data cannot be determined. Please define the "type" parameter.',
                       details='')
        return True

    def prepare_single_data(self):
        ''' Gets data from original_data1 and original_data2 and send
            to calculate
        '''
        # Clear current data:
        self.data_for_calculations = []
        # Get data from self.original_data1
        x_data1 = copy.deepcopy(self.original_data1.x)
        y_data1 = copy.deepcopy(self.original_data1.y)
        z_data1 = copy.deepcopy(self.original_data1.z)
        name1 = copy.deepcopy(self.original_data1.name)
        # Extract the data in x and y
        x_data1, y_data1 = self.extract_region_xy(x = x_data1, y = y_data1)
        data_1 = {'x':x_data1, 'y':y_data1, 'name':name1}
        self.data_for_calculations.append(data_1)
        if self.use_second:
            # Check if the second selected data is single 2D
            is_2D = self.original_data2.y.ndim == 2
            if self.original_data2.type.lower() != 'single 2D' or is_2D != 2:
                # First is single 2D and second is single 2D
                x_data2 = copy.deepcopy(self.original_data2)
                y_data2 = copy.deepcopy(self.original_data2)
                z_data2 = copy.deepcopy(self.original_data2)
                name2 = copy.deepcopy(self.original_data2.name)
                # Extract the data in x and y
                x_data2, y_data2 = self.extract_region_xy(x=x_data2, y=y_data2)
                data_2 = {'x': x_data2, 'y': y_data2, 'name': name2}
                self.data_for_calculations.append(data_2)
            else:
                Error.show(info='If the first data is 2D, the second must also be 2D, not a stack.', details='')
                return False
        return True

    def prepare_stack_for_calc(self):
        print("to be done stack as whole")
        return False

    def prepare_for_stack_separate(self):
        print("to be done stack_separate")

    #
    #   UPDATING RESULTS
    #

    def update_result_data(self, y=None, x=None, z=None):
        ''' Move calculated data in y and x to self.eleana.result_dataset. '''
        # Update results if there was a single data
        if y is not None:
            if self.app:
                if self.original_data.type.lower() == "stack 2d":
                    if self.auto_result:
                        self.result_data.y[self.i_stk]  = y
                else:
                    if self.auto_result:
                        self.result_data.y = y
            else:
                print('Result Y:')
                print(y)
        if x is not None:
            if self.app:
                if self.auto_result:
                    self.result_data.x = x
            else:
                print('Result X:')
                print(x)
        if z is not None:
            if self.app:
                if self.auto_result:
                    self.result_data.z = z
            else:
                print('Result Z:')
                print(z)

    def prep_calc_data(self, x=None, y=None, z=None, name=None, region = None):
        ''' Master methods which takes data either from self.original of from given x, y, x args'''
        if isinstance(y, np.ndarray) and y.ndim != 1:
            self.eleana.cmd_error = 'Y must be one-dimensional.'
            return None, None, None, None, None, None, None, None
        elif isinstance(y, list) and all(not isinstance(i, list) for i in y):
            self.eleana.cmd_error = 'Y must be one-dimensional.'
            return None, None, None, None, None, None, None, None
        # Prepare data for calculation depending x,y,z
        if region is not None:
            if not isinstance(region, list):
                self.eleana.cmd_error = 'Region argument must be a list with exactly 2 elements'
                return None,None,None,None,None,None,None,None
            elif isinstance(region, list) and len(region) != 2:
                self.eleana.cmd_error = 'Region argument must be a list with exactly 2 elements'
                return None,None,None,None,None,None,None,None
            elif isinstance(region, list) and any(isinstance(sublist, list) and len(sublist) != 2 for sublist in region):
                self.eleana.cmd_error = 'Region argument must be a list of lists, each containing exactly 2 elements'
                return None,None,None,None,None,None,None,None

        if x is None:
            # Prepare data directly from self.original_data
            x_data, y_data, z_data, name, x_cal, y_cal, z_cal, name_cal = self.prep_from_original_data(region=region)
            if len(x_data) == 0:
                Error.show(info = f'There is no data between selected range for {name}')
                return None,None,None,None,None,None,None
        else:
            x_data, y_data, z_data, name, x_cal, y_cal, z_cal, name_cal = self.prep_from_xyz(x = x, y = y, z = z, name=name, region=region)
        if not x_data.all() and self.batch:
            self.eleana.cmd_error = 'There is no data within the region.'
        x_data = np.asarray(x_data)
        y_data = np.asarray(y_data)
        z_data = np.asarray(z_data)
        return x_data, y_data, z_data, name, x_cal, y_cal, z_cal, name_cal

    def prep_from_xyz(self, x, y, z=None, name=None, region=None):
        ''' Prepare x_data, y_data, z_data to use for calculations from given x,y,z'''
        if region is not None:
            extracted_x, extracted_y = self.extract_region_xy_cmd(x,y, region)
        elif self.get_from_region and self.eleana is not None:
            extracted_x, extracted_y = self.extract_region_xy(x,y)
        else:
            extracted_x = x
            extracted_y = y
        x_data = extracted_x
        y_data = extracted_y
        z_data = z
        x_cal = copy.deepcopy(x_data)
        y_cal = copy.deepcopy(y_data)
        z_cal = copy.deepcopy(z_data)
        name_cal = copy.deepcopy(name)
        return x_data, y_data, z_data, name, x_cal, y_cal, z_cal, name_cal

    def prep_from_original_data(self):
        ''' Prepare x_data, y_data, z_data to use for calculations from self.original_data '''
        if region is not None:
            print('Region is defined for prep_from_original_data')
        if self.get_from_region:
            self.extract_region()
        x_data = self.original_data.x
        y_data = self.original_data.y
        z_data = self.original_data.z
        name = self.original_data.name_nr
        x_cal = copy.deepcopy(x_data)
        y_cal = copy.deepcopy(y_data)
        z_cal = copy.deepcopy(z_data)
        name_cal = copy(name)
        if len(x_data) == 0:
            self.get_data(None, None)
            if self.get_from_region:
                self.extract_region()
            x_data = self.original_data.x
            y_data = self.original_data.y
            z_data = self.original_data.z
            name = self.original_data.name_nr
            if self.get_from_region:
                self.extract_region()
            x_cal = x_data
            y_cal = y_data
            z_cal = z_data
            name_cal = name
        return x_data, y_data, z_data, name, x_cal, y_cal, z_cal, name_cal


    def single_calc_workflow(self, value=None):
        ''' Master method triggered by clicking "OK" or "calculate" button  '''
        if self.original_data is None:
            if self._data_label__ is not None:
                self._data_label__.configure(text = '')
            return
        if self.original_data.type.lower() == "stack 2d":
            self.extract_from_result()
            if self.stack_sep:
                # Store current create_report status
                create_report = copy.copy(self.create_report)
                self.i_stk = 0
                self.create_report = True
                for each in self.original_data.stk_names:
                    name_ = self.original_data.name_nr + '/' + each
                    x_ = self.original_data.x
                    y_ = self.original_data.y[self.i_stk]
                    z_ = self.original_data.z[self.i_stk]
                    if self._data_label__ is not None:
                        self._data_label__.configure(text = name_)
                        # Update tkinter widget
                        if self.update_gui:
                            self.app.mainwindow.update()
                            pass
                    calc_result_row = self.calculate(x = x_, y = y_, z = z_, name = name_, stk_index = self.i_stk)
                    try:
                        self.add_to_report(row = calc_result_row)
                    except ValueError:
                        break
                    self.i_stk+=1
                    self.consecutive_number += 1
                # Restore create_report_settings
                self.create_report = create_report
            else:
                name_ = self.original_data.name_nr
                x_ = self.original_data.x
                y_ = self.original_data.y
                if self._data_label__ is not None:
                    self._data_label__.configure(text=name_)
                    # Update tkinter widget
                    if self.update_gui:
                        self.app.mainwindow.update()
                calc_result_row = self.calculate_stack(x = x_, y = y_, z = None, name = name_, stk_index = None)
                if self.create_report:
                    self.add_to_report(row = calc_result_row)
            #if self.show_stk_report:
            #    self.show_report()
        elif self.original_data.type.lower() == 'single 2d':
            name_ = self.original_data.name_nr
            if self._data_label__ is not None:
                self._data_label__.configure(text=name_)
                if self.update_gui:
                    self.app.mainwindow.update()
                pass
            x_ = self.original_data.x
            y_ = self.original_data.y
            z_ = self.original_data.z
            name_ = self.original_data.name_nr
            try:
                calc_result_row = self.calculate(name = name_, y = y_, x = x_, z = z_)
                self.add_to_report(row=calc_result_row)
            except ValueError:
                if self.process_group_show_error:
                    answer = Error.ask_for_option(title = 'Empty range',
                                                  info = f"There is no data in: \n\n {name_}\n\n within the selected range. \n\nIf you don’t want this error to appear for other data in the group, click the SKIP button.",
                                                  option = "Skip")
                    if answer == 'Skip':
                        self.process_group_show_error = False
                    else:
                        self.process_group_show_error = True

    def perform_group_calculations(self, headers = None):
        selections_copy = copy.deepcopy(self.eleana.selections)
        self.get_data()
        self.grapher.canvas.get_tk_widget().config(cursor="watch")
        self.app.mainwindow.configure(cursor="watch")
        try:
            self.group_calc_workflow()
            self.app.result_show()
        except Exception as e:
            print(e)
        self.grapher.canvas.get_tk_widget().config(cursor="")
        self.app.mainwindow.configure(cursor="")
        self.eleana.selections = selections_copy
        self.app.gui_set_from_eleana()
        if self.create_report:
            self.show_report()

    def group_calc_workflow(self, headers = None):
        ''' Triggers 'perform_calculation' for all data in the current group. '''
        self.update_gui = False
        self.process_group_show_error = True
        self.show_stk_report = False
        self.collected_reports['rows'] = []
        self.app.clear_results(skip_question=True, refresh_graph = False)
        spectra = copy.copy(self.app.sel_first._values)
        del spectra[0]
        i = 0
        keep_selections = copy.deepcopy(self.eleana.selections)
        for spectrum in spectra:
            self.app.first_to_result(name=spectrum, refresh_graph=False)
            index = self.eleana.get_index_by_name(spectrum)
            self.eleana.selections['first'] = index
            self.original_data = copy.deepcopy(self.eleana.dataset[index])
            if self.auto_result:
                self.result_data = self.eleana.results_dataset[i]
            self.extract_region()
            self.single_calc_workflow()
            i += 1
            self.consecutive_number+=1
        self.mainwindow.config(cursor='')
        #if self.create_report:
        #    self.show_report()
        self.eleana.selections = keep_selections
        self.process_group_show_error = True
        self.update_gui = True
        self.grapher.canvas.get_tk_widget().config(cursor="")
        self.app.mainwindow.configure(cursor="")

    def place_annotation(self, x, y = None, which = 'first', style = None):
        ''' Sets the annotation at given point.
            If only x is set the y coordinate will snap to the curve indicated in "which" variable.
            If x and y are set then the annotation will appear at given (x,y) coordinates
            '''
        if x is None:
            return
        if y:
            snap = False
        else:
            snap = True
        self.grapher.set_custom_annotation(point = (x,y), snap=snap, which = which)
        self.grapher.updateAnnotationList()
        self.grapher.draw_plot()

    def add_to_report(self, headers = None, row = None):
        ''' Add headers for columns and or additional row to the report'''
        if headers:
            self.collected_reports['headers'] = headers
        if row:
            if len(row) != len(self.collected_reports['headers']):
                if self.eleana.devel_mode:
                    Error.show(title="Error in report creating.", info="The number of column headers is different than provided columns in row. See console for details")
                    raise ValueError
            else:
                processed_row = []
                for item in row:
                    if item is None:
                        item = ''
                    processed_row.append(item)
                self.collected_reports['rows'].append(processed_row)

    def show_report(self):
        ''' Display report as Table a table'''
        if not self.collected_reports:
            if self.eleana.devel_mode:
                print("There is no reports in self.collected_reports")
            return
        rows = self.collected_reports['rows']
        headers = self.collected_reports['headers']
        df = pandas.DataFrame(rows, columns=headers)
        default_x = self.collected_reports['default_x']
        default_y = self.collected_reports['default_y']
        x_unit = self.collected_reports['x_unit']
        x_name = self.collected_reports['x_name']
        y_name = self.collected_reports['y_name']
        y_unit = self.collected_reports['y_unit']

        table = CreateFromTable(window_title="Results of integration",
                                eleana_app=self.eleana,
                                master=self.mainwindow,
                                df=df,
                                name='Results of Integration',
                                default_x_axis=default_x,
                                default_y_axis=default_y,
                                x_unit = x_unit,
                                x_name = x_name,
                                y_unit = y_unit,
                                y_name = y_name,
                                group=self.report_to_group)
        response = table.get()
        self.update.dataset_list()
        self.update.group_list()
        self.update.all_lists()

    def clear_report(self):
        ''' Clear the created report '''
        self.collected_reports['rows'] = []
        self.consecutive_number = 1

    def extract_region_xy(self, x, y):
        ''' Extract data using selected range (self.grapher.color_span) or scale (x_min, x_max) from array in x,y '''
        if self.regions['from'] == 'scale':
            ranges = [self.grapher.ax.get_xlim()]
        elif self.regions['from'] == 'selection':
            ranges = self.eleana.color_span['ranges']
        else:
            print('REGIONS_FROM must be "scale", "selection" or "none"')
            return x, y
        if ranges == []:
            return x, y
        indexes = []
        for range_ in ranges:
            idx = np.where((x >= range_[0]) & (x <= range_[1]))[0]
            indexes.extend(idx.tolist())
        extracted_x = x[indexes]
        extracted_y = y[indexes]
        return extracted_x, extracted_y

    def extract_from_result(self):
        ''' Extract data in results according to ranges in self.eleana.color_span
            when result_data.y is a stack
        '''
        x_ = self.result_data.x
        extracted_y = []
        for each_y in self.result_data.y:
            x_, y_ = self.extract_region_xy(x = x_, y=each_y)
            extracted_y.append(y_)
        y_ = np.asarray(extracted_y)
        self.result_data.y = y_
        self.result_data.x = x_

    def extract_region_xy_cmd(self, x, y, region):
        ''' Extract data using range passed from command line '''
        ranges = region
        if ranges == []:
            return x, y
        is_2D = isinstance(ranges, list) and all(isinstance(r, (list, np.ndarray)) for r in ranges)
        if not is_2D:
            ranges = [region]
        indexes = []
        for range_ in ranges:
            range_ = sorted(range_)
            idx = np.where((x >= range_[0]) & (x <= range_[1]))[0]
            indexes.extend(idx.tolist())
        extracted_x = x[indexes]
        try:
            extracted_y = y[indexes]
            return extracted_x, extracted_y
        except IndexError:
            self.eleana.cmd_error = 'Y array must be a one-dimensional'
            return [],[]

    def extract_region(self, x=None, y=None):
        ''' Same as extract_region_xy but from self.original_data '''
        if self.region_from_scale:
            ranges = [self.grapher.ax.get_xlim()]
        else:
            ranges = self.eleana.color_span['ranges']
        if ranges == []:
            return
        if self.original_data:
            x = self.original_data.x
            y = self.original_data.y
            is_2D = len(y.shape) == 2
            indexes = []
            for range_ in ranges:
                idx = np.where((x >= range_[0]) & (x <= range_[1]))[0]
                indexes.extend(idx.tolist())
            extracted_x = x[indexes]
            if is_2D:
                extracted_y = y[:, indexes]
            else:
                extracted_y = y[indexes]
            self.original_data.x = extracted_x
            self.original_data.y = extracted_y
        if self.original_data2:
            # Extract for second
            if self.use_second:
                x = self.original_data2.x
                y = self.original_data2.y
                is_2D = len(y.shape) == 2
                indexes = []
                for range_ in ranges:
                    idx = np.where((x >= range_[0]) & (x <= range_[1]))[0]
                    indexes.extend(idx.tolist())
                extracted_x = x[indexes]
                if is_2D:
                    extracted_y = y[:, indexes]
                else:
                    extracted_y = y[indexes]
                self.original_data2.x = extracted_x
                self.original_data2.y = extracted_y
        if self.auto_result:
            x = self.result_data.x
            y = self.result_data.y
            is_2D = len(y.shape) == 2
            indexes = []
            for range_ in ranges:
                idx = np.where((x >= range_[0]) & (x <= range_[1]))[0]
                indexes.extend(idx.tolist())
            extracted_x = x[indexes]
            if is_2D:
                extracted_y = y[:, indexes]
            else:
                extracted_y = y[indexes]
            self.result_data.x = extracted_x
            self.result_data.y = extracted_y

    def extract_region_cmd(self, range):
        ranges = range
        if ranges == []:
            return
        if self.original_data:
            x = self.original_data.x
            y = self.original_data.y
            is_2D = len(y.shape) == 2
            indexes = []
            for range_ in ranges:
                idx = np.where((x >= range_[0]) & (x <= range_[1]))[0]
                indexes.extend(idx.tolist())
            extracted_x = x[indexes]
            if is_2D:
                extracted_y = y[:, indexes]
            else:
                extracted_y = y[indexes]
            self.original_data.x = extracted_x
            self.original_data.y = extracted_y
        if self.original_data2:
            # Extract for second
            if self.use_second:
                x = self.original_data2.x
                y = self.original_data2.y
                is_2D = len(y.shape) == 2
                indexes = []
                for range_ in ranges:
                    idx = np.where((x >= range_[0]) & (x <= range_[1]))[0]
                    indexes.extend(idx.tolist())
                extracted_x = x[indexes]
                if is_2D:
                    extracted_y = y[:, indexes]
                else:
                    extracted_y = y[indexes]
                self.original_data2.x = extracted_x
                self.original_data2.y = extracted_y
        if self.auto_result:
            x = self.result_data.x
            y = self.result_data.y
            is_2D = len(y.shape) == 2
            indexes = []
            for range_ in ranges:
                idx = np.where((x >= range_[0]) & (x <= range_[1]))[0]
                indexes.extend(idx.tolist())
            extracted_x = x[indexes]
            if is_2D:
                extracted_y = y[:, indexes]
            else:
                extracted_y = y[indexes]
            self.result_data.x = extracted_x
            self.result_data.y = extracted_y

    ''' Several general methods to handle GUI elements like Validation 
        method for CTkEntry or putting the value to the disabled CTkEntry '''

    # Section handling CTkEntries
    def set_validation_for_ctkentries(self, list_of_entries):
        ''' Sets the validation methods for the CTkEntries listed in "list_of_entries"  '''
        self.validate_command = (self.mainwindow.register(self.validate_number), '%P')
        for entry in list_of_entries:
            entry.configure(validate="key", validatecommand=self.validate_command)

    def validate_number(self, new_value):
        """ Validates that the input is a number or empty.
         Called on each keystroke in CTkEntry fields with `validate="key"`.
        """
        # Handle empty field
        if new_value == '':
            return True
        # Check if entry can be converted to float
        try:
            float(new_value)  # OK
            return True
        except ValueError:
            return False

    def set_entry_value(self, entry=None, value=None):
        ''' Puts the "value" int the field of CTkEntry defined by "entry" '''
        if entry is None:
            return
        if entry.cget("state") == "disabled":
            entry.configure(state = 'normal')
            entry.delete(0, 'end')
            entry.insert(0, str(value))
            entry.configure(state = 'disabled')
        else:
            entry.delete(0, 'end')
            entry.insert(0, str(value))

    def set_mouse_state(self, state = ""):
        self.grapher.canvas.get_tk_widget().config(cursor=state)
        self.app.mainwindow.configure(cursor=state)
