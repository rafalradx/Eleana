from assets.Observer import Observer
import copy
import numpy as np
from assets.Error import Error
from subprogs.table.table import CreateFromTable
import pandas

class SubMethods():
    def __init__(self, app=None, which='first', use_second = False, stack_sep = True, data_label = None, work_on_start = False, window_title='', on_top = True, cursor_mode=None):
        # Set get_from_region to use selected range for data
        #self.collected_reports = None
        self.original_data = None
        self.original_data2 = None
        self.get_from_region = True
        self.consecutive_number = 1
        self.data_name_widget = None
        self.show_stk_report = True
        self.work_on_start = work_on_start
        if app:
            self.batch = False
            self.mainwindow.protocol('WM_DELETE_WINDOW', self.cancel)
            self.app = app
            self.master = self.app.mainwindow
            self.eleana = self.app.eleana
            self.grapher = self.app.grapher
            self.update = self.app.update
            self.mainwindow.title(window_title)
            self.mainwindow.attributes('-topmost', on_top)
            if data_label is not None:
                data_label_text = "self._data_label__ = self.builder.get_object(" + data_label + ", self.mainwindow)"
                exec(data_label_text)
            else:
                self._data_label__ = None
            if cursor_mode is not None:
                self.grapher.cursor_limit = cursor_mode['limit']
                self.app.sel_graph_cursor(cursor_mode['type'])
                self.app.sel_cursor_mode.set(cursor_mode['type'])
        else:
            self.app = None
            self.master = None
            self.eleana = None
            self.grapher = None
            self.batch = True
        # Set to which selection 'First' or 'Second'
        self.which = which
        self.use_second = use_second
        self.stack_sep = stack_sep
        # Do not build window if app is not defined
        if self.app:
            # Create window
            self.configure_window()
            # Create observer
            self.observer = Observer(self.eleana, self)
            self.eleana.notify_on = True
            # Initialize data to modify
            self.get_data(start=True)
            # Set current position in Results Dataset
            self.result_index = len(self.eleana.results_dataset)

    def get(self):
        ''' Returns self.response to the main application after close '''
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event=None):
        ''' Close the window without changes '''
        self.response = None
        # Unregister observer
        self.eleana.detach(self.observer)
        self.mainwindow.destroy()

    def get_data(self, start=False):
        ''' Makes a copy of the selected data and stores it in self.original_data.
            You may perform calculations on self.original_data. '''
        # Get data from selections First or Second
        if self.eleana.selections[self.which] >= 0:
            index = self.eleana.selections[self.which]
            if not start:
                self.eleana.notify_on = False
            if self.which == 'second':
                self.app.second_to_result()
            else:
                self.app.first_to_result()
        else:
            self.original_data = None
            self.result_data = None
            return False
        if self.use_second:
            # --- TWO DATA ARE NEEDED ---
            index = self.eleana.selections['first']
            index2 = self.eleana.selections['second']
            if index == -1:
                if self.app:
                    Error.show(info='No first data selected', details='')
                self.original_data = None
                return False
            elif self.eleana.selections['second'] == -1:
                if self.app:
                    Error.show(info='No second data selected', details='')
                self.original_data2 = None
                return False
            self.original_data2 = copy.deepcopy(self.eleana.dataset[index2])
            self.original_data = copy.deepcopy(self.eleana.dataset[index])
        else:
            # --- ONLY ONE DATA IS NEEDED ---
            # Create reference to original data
            self.original_data = copy.deepcopy(self.eleana.dataset[index])
            self.original_data2 = None
        # Create reference to data in results
        self.result_index = self.eleana.selections['result']
        self.result_data = self.eleana.results_dataset[self.result_index]
        if self.get_from_region:
            self.extract_region()
        if self.work_on_start:
            self.perform_single_calculations()

    def data_changed(self):
        ''' Activate get_data when selection changed.
            This is triggered by the Observer.   '''
        self.get_data()
        self.perform_single_calculations()

    def update_result_data(self, y=None, x=None, z=None):
        ''' Move calculated data in y and x to self.eleana.result_dataset. '''

        # Update results if there was a single data
        if y is not None:
            if self.app:
                if self.original_data.type.lower() == "stack 2d":
                    self.result_data.y[self.i_stk]  = y
                else:
                    self.result_data.y = y
            else:
                print('Result Y:')
                print(y)
        if x is not None:
            if self.app:
                self.result_data.x = x
            else:
                print('Result X:')
                print(x)
        if z is not None:
            if self.app:
                self.result_data.z = z
            else:
                print('Result Z:')
                print(z)
        if self.app:
            self.grapher.plot_graph()
    def prep_calc_data(self, dataset, x_data, y_data, z_data, name):
        if self.get_from_region:
            self.extract_region()
        if dataset and self.app is None:
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
    def perform_single_calculations(self, value=None):
        if self.original_data is None:
            if self._data_label__ is not None:
                self._data_label__.configure(text = '')
            return
        if self.original_data.type.lower() == "stack 2d":
            if self.stack_sep:
                # Store current create_report status
                self.mainwindow.config(cursor='watch')
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
                    calc_result_row = self.calculate(x = x_, y = y_, z = z_, name = name_, stk_index = self.i_stk)
                    try:
                        self.add_to_report(row = calc_result_row)
                    except ValueError:
                        break
                    self.i_stk+=1
                    self.consecutive_number += 1
                # Restore create_report_setings
                self.create_report = create_report
            else:
                name_ = self.original_data.name_nr
                x_ = self.original_data.x
                y_ = self.original_data.y
                if self._data_label__ is not None:
                    self._data_label__.configure(text=name_)
                calc_result_row = self.calculate_stack(x = x_, y = y_, z = None, name = name_, stk_index = None)
                if self.create_report:
                    self.add_to_report(row = calc_result_row)
            self.mainwindow.config(cursor='')
            if self.show_stk_report:
                self.show_report()
        elif self.original_data.type.lower() == 'single 2d':
            name_ = self.original_data.name_nr
            if self._data_label__ is not None:
                self._data_label__.configure(text=name_)
            calc_result_row = self.calculate(name = self.original_data.name_nr, y = self.original_data.y, x = self.original_data.x)
            self.add_to_report(row=calc_result_row)

    def perform_group_calculations(self, headers = None):
        ''' Triggers 'perform_calculation' for all data in the current group. '''
        self.show_stk_report = False
        self.collected_reports['rows'] = []
        self.app.clear_results(skip_question=True)
        self.mainwindow.config(cursor='watch')
        spectra = copy.copy(self.app.sel_first._values)
        del spectra[0]
        i = 0
        keep_selections = copy.deepcopy(self.eleana.selections)
        for spectrum in spectra:
            self.app.first_to_result(name=spectrum)
            index = self.eleana.get_index_by_name(spectrum)
            self.eleana.selections['first'] = index
            self.original_data = copy.deepcopy(self.eleana.dataset[index])
            self.result_data = self.eleana.results_dataset[i]
            self.perform_single_calculations()
            i += 1
            self.consecutive_number+=1
        self.mainwindow.config(cursor='')
        if self.create_report:
            self.show_report()
        self.eleana.selections = keep_selections

    def add_to_report(self, headers = None, row = None):
        ''' Add headers for columns and or additional row to the report'''
        if headers:
            self.collected_reports['headers'] = headers
        if row:
            if len(row) != len(self.collected_reports['headers']):
                if self.eleana.devel_mode:
                    Error.show(title="Error in report creating.", info="The number of column headers is different than provided columns in row. See console for details")
                    print('The number of columns does not equal the column headers:')
                    print('headers = ', self.collected_reports['headers'])
                    print('row = ', row)
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
        group = self.eleana.selections['group']
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
                                group=group)
        response = table.get()
        self.update.dataset_list()
        self.update.group_list()
        self.update.all_lists()

    def clear_report(self):
        self.collected_reports['rows'] = []
        self.consecutive_number = 1

    def extract_region(self, x=None, y=None):
        ''' Extract data on the basis of selected ranges in self.eleana.color_span['ranges'] '''
        ranges = self.eleana.color_span['ranges']
        if not ranges:
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

    def set_validation_for_ctkentries(self, list_of_entries):
        self.validate_command = (self.mainwindow.register(self.validate_number), '%P')
        for entry in list_of_entries:
            entry.configure(validate="key", validatecommand=self.validate_command)

    def validate_number(self, new_value):
        """
        Validates that the input is a number or empty.
        Called on each keystroke in CTkEntry fields with `validate="key"`.

        Args:
        - new_value (str): The current content of the entry field.

        Returns:
        - bool: True if `new_value` is a valid number or empty, False otherwise.
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