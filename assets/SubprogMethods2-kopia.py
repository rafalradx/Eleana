

from assets.Observer import Observer
import copy
import numpy as np
from assets.Error import Error
from subprogs.table.table import CreateFromTable
import pandas


class SubMethods_02:
    def __init__(self, app=None, which='first', commandline=False):
        self.commandline = commandline
        self.general_error_skip = False
        self.update_gui = True
        self.data_for_calculations = []
        self.consecutive_number = 1

        if app and not self.commandline:
            # Window start from Menu in GUI
            self.app = app
            self.mainwindow.protocol('WM_DELETE_WINDOW', self.cancel)
            self.master = self.app.mainwindow
            self.eleana = self.app.eleana
            self.grapher = self.app.grapher
            self.update = self.app.update
            self.mainwindow.title(self.subprog_settings['title'])
            self.mainwindow.attributes('-topmost', self.subprog_settings['on_top'])
            if self.subprog_settings['data_label']:
                self.data_label = self.builder.get_object(self.subprog_settings['data_label'], self.mainwindow)
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
            # Custom window configuration in parent
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


    # STANDARD METHODS FOR MAIN APPLICATION
    # ----------------------------------------------

    def get(self):
        ''' Returns self.response to the main application after close '''
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event=None):
        ''' Close the window with self.response = None '''
        self.response = None
        # Return cursor selection to enabled
        self.app.sel_cursor_mode.configure(state="normal")
        self.app.sel_cursor_mode.set(self.subprog_cursor['previous'])
        self.app.sel_graph_cursor(self.subprog_cursor['previous'])
        # Unregister observer
        self.eleana.detach(self.observer)
        self.grapher.clear_selected_ranges()
        self.mainwindow.destroy()



    # GETTING THE DATA ACCORDING TO ELEANA.SELECTION
    # ----------------------------------------------

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
            self.app.mainwindow.configure(cursor="")
            self.grapher.canvas.get_tk_widget().config(cursor="")
            return False
        elif variable == "grapher_action":
            return False
        elif variable == 'result':
            return False
        if self.subprog_settings['auto_calculate']:
            self.ok_clicked()
        return True


    # STANDARD METHODS FOR SUBPROG GUI BUTTONS
    #

    def ok_clicked(self):
        ''' [-OK-] button
            This is standard function in SubprogMethods '''
        self.start_single_calculations()

    def process_group_clicked(self):
        ''' [-Process Group-] button
            This is standard function in SubprogMethods '''
        self.perform_group_calculations()

    def show_report_clicked(self):
        ''' [-Show Report-] button
            This is standard function in SubprogMethods '''
        self.show_report()

    def clear_report_clicked(self):
        ''' [-Show Report-] button
            This is standard function in SubprogMethods '''
        self.clear_report()



    # TRIGGERING CALCULATIONS
    # -----------------------------------------------

    def start_single_calculations(self):
        ''' This function is triggered by clicking "Calculate" button'''
        self.skip_next_error = False
        status = self.get_data()
        if status:
            self.perform_single_calculations(group_processing=False)

    def perform_single_calculations(self, group_processing=False):
        ''' Prepares for calculations of single data selected in First or Second
            This function checks if this is a single data of stack and if stack
            can be calculated as separate data or must be taken as whole.
            This function is triggered by Clicking "Calculate" or data change in GUI
        '''

        skip_report_show = True
        self.set_mouse_state("watch")
        # Create result_dataset if add or replace is set
        if self.subprog_settings['result'] == 'add':
            # Simply add the result to the eleana.results_dataset
            self.result_data = copy.deepcopy(self.original_data1)
            # Extract data from selections:
            extr_x, extr_y = self.extract_region_xy(self.result_data.x, self.result_data.y)
            self.result_data.x = extr_x
            self.result_data.y = extr_y
            self.result_data.name = self.result_data.name + self.subprog_settings['name_suffix']
            self.result_data.name_nr = self.result_data.name_nr + self.subprog_settings['name_suffix']
            self.eleana.results_dataset.append(self.result_data)
            self.current_index_in_results = len(self.eleana.results_dataset) - 1

        elif self.subprog_settings['result'] == 'replace':
            # The replace mode was set
            self.result_data = copy.deepcopy(self.original_data1)
            # Extract data from selections:
            extr_x, extr_y = self.extract_region_xy(self.result_data.x, self.result_data.y)
            self.result_data.x = extr_x
            self.result_data.y = extr_y

            self.result_data.name = self.result_data.name + self.subprog_settings['name_suffix']
            if len(self.eleana.results_dataset) == 0:
                # Results_dataset is empty so new_result must be added
                self.result_data = copy.deepcopy(self.original_data1)
                # Extract data from selections:
                extr_x, extr_y = self.extract_region_xy(self.result_data.x, self.result_data.y)
                self.result_data.x = extr_x
                self.result_data.y = extr_y
                self.result_data.name = self.result_data.name + self.subprog_settings['name_suffix']
                self.eleana.results_dataset.append(self.result_data)
                self.current_index_in_results = 0
            else:
                # Replace the last data in results_dataset
                self.current_index_in_results = len(self.eleana.results_dataset) - 1
                self.eleana.results_dataset[self.current_index_in_results] = self.result_data
        else:
            # Do not create results
            self.result_data = None
            self.current_index_in_results = - 1

        is_2D = self.original_data1.y.ndim == 2
        # Check if data is stack 2D
        if self.original_data1.type.lower() == 'stack 2D' or is_2D:
            # This is stack 2D then check if stack is calculated as separate data
            self.stk_index = 0
            if not self.stack_sep:
                status = self.stack_calc() # Prepare the whole stack for calculations
                if not status:
                    return status
            else:
                # Single data but it is a stack that use separate calculations
                # Iterate over stk
                name_nr = self.original_data1.name_nr + self.subprog_settings['name_suffix']
                for stk_name in self.original_data1.stk_names:
                    name = name_nr + '/' + stk_name + self.subprog_settings['name_suffix']
                    if self.data_label is not None:
                        self.data_label.configure(text=name)
                        self.app.mainwindow.update()
                        status = self.do_calc_stk_data()
                        if status:
                            self.consecutive_number += 1
                            self.stk_index += 1
                        else:
                            return status
                # After stk calculations
                self.stk_index = -1
                self.set_mouse_state("")
                skip_report_show = False

        # Single data that is not a stack
        elif self.original_data1.type.lower() == 'single 2D' or not is_2D:
            self.stk_index = -1
            if self.data_label is not None:
                self.data_label.configure(text=self.original_data1.name_nr)
                self.app.mainwindow.update()
                status = self.do_calc_single2D()
                if status:
                    self.consecutive_number += 1
                else:
                    return status
            skip_report_show = True

        else:
            Error.show(info='The type of the selected data cannot be determined. Please define the "type" parameter.',
                       details='')

        if group_processing:
            # If group processing is activated skip GUI update
            return True
        else:
            if len(self.eleana.results_dataset) == 0:
                self.show_report()
                return True
            else:
                # Select result to the last enrty
                list_of_results = self.app.sel_result._values
                selected_value_text = list_of_results[-1]
                self.app.result_selected(selected_value_text)
                self.app.sel_result.set(selected_value_text)
        if not skip_report_show:
            self.show_report()
        return True

    def perform_group_calculations(self):
        # Make copy of the settings and eleana.selections
        copy_selections = copy.deepcopy(self.eleana.selections)
        copy_of_subprog_settings = copy.deepcopy(self.subprog_settings)

        # Clear the whole results_dataset and report
        self.eleana.results_dataset = []
        self.clear_report()

        # Prepare settings for group processing
        current_group = self.eleana.selections['group']
        if current_group == "All":
            group_list = tuple(range(len(self.eleana.dataset)))
        else:
            group_list = self.eleana.assignmentToGroups[current_group]
        self.subprog_settings['result'] = 'add'

        # Do the single calculation for the each of the data in the
        for each in group_list:
            self.eleana.selections['first'] = each
            status1 = self.get_data()
            if status1:
                status2 = self.perform_single_calculations(group_processing=True)
                if not status2:
                    self.eleana.selections = copy_selections
                    self.subprog_settings = copy_of_subprog_settings
                    self.show_results_matching_first()
                    return False

        # After processing
        self.eleana.selections = copy_selections
        self.subprog_settings = copy_of_subprog_settings

        # Display result settings that match selection in first
        self.show_results_matching_first()

        # Show Report
        self.show_report()

    def do_calc_stk_data(self):
        ''' Gets each stk from stack 2D and send to calculate '''
        # Clear current working data and prepare result if needed:
        self.data_for_calculations = []

        # Get data from self.original_data1
        x_data1 = copy.deepcopy(self.original_data1.x)
        y_data1 = copy.deepcopy(self.original_data1.y[self.stk_index])
        z_data1 = copy.deepcopy(self.original_data1.z)
        name1 = copy.deepcopy(self.original_data1.name)
        name1 = name1 + '/' + copy.deepcopy(self.original_data1.stk_names[self.stk_index])
        complex1 = copy.deepcopy(self.original_data1.complex)
        datatype1 = copy.deepcopy(self.original_data1.type)
        origin1 = copy.deepcopy(self.original_data1.origin)
        comment1 = copy.deepcopy(self.original_data1.comment)
        parameters1 = copy.deepcopy(self.original_data1.parameters)


        # Extract the data in x and y if needed
        x_data1, y_data1 = self.extract_region_xy(x=x_data1, y=y_data1)
        if y_data1.size == 0:
            Error.show(info=f'For the selected range, the {name1} contains no values')
            self.set_mouse_state(state='')
            self.show_results_matching_first()
            return False
        data_1 = {'x': x_data1,
                  'y': y_data1,
                  'z': z_data1,
                  'name': name1,
                  'stk_value':z_data1[self.stk_index],
                  'complex':complex1,
                  'type':datatype1,
                  'origin':origin1,
                  'comment':comment1,
                  'parameters':parameters1
                  }
        self.data_for_calculations.append(data_1)
        if self.use_second:
            # Check if the second selected data is single 2D
            is_2D = self.original_data2.y.ndim == 2
            if self.original_data2.type.lower() != 'single 2D' or is_2D != 2:
                # First is single 2D and second is single 2D
                x_data2 = copy.deepcopy(self.original_data2.x)
                y_data2 = copy.deepcopy(self.original_data2.y)
                z_data2 = copy.deepcopy(self.original_data2.z)
                name2 = copy.deepcopy(self.original_data2.name)
                complex2 = copy.deepcopy(self.original_data1.complex)
                datatype2 = copy.deepcopy(self.original_data1.type)
                origin2 = copy.deepcopy(self.original_data1.origin)
                comment2 = copy.deepcopy(self.original_data1.comment)
                parameters2 = copy.deepcopy(self.original_data1.parameters)
                # Extract the data in x and y
                x_data2, y_data2 = self.extract_region_xy(x=x_data2, y=y_data2)
                if y_data2.size == 0:
                    return False
                try:
                    # Exception called when number of z_data1 is different than z_data2
                    # thus 'stk_value' cannot be created by iteration
                    data_2 = {'x': x_data2,
                              'y': y_data2,
                              'z': z_data2,
                              'name': name2,
                              'stk_value':z_data2[self.stk_index],
                              'complex': complex2,
                              'type': datatype2,
                              'origin': origin2,
                              'comment': comment2,
                              'parameters': parameters2
                              }
                except:
                    # Skip setting 'stk_value'
                    data_2 = {'x': x_data2,
                              'y': y_data2,
                              'z': z_data2,
                              'name': name2,
                              'stk_value':'',
                              'complex':complex2,
                              'type': datatype2,
                              'origin': origin2,
                              'comment': comment2,
                              'parameters': parameters2
                              }
                self.data_for_calculations.append(data_2)
            else:
                Error.show(info='If the first data is 2D, the second must also be 2D, not a stack.', details='')
                return False
        else:
            self.data_for_calculations.append(None)
        # Go to calculate function
        row_to_report = self.calculate()
        # Update data and report
        if isinstance(row_to_report, list):
            if self.report['create']:
                self.add_to_report(row=row_to_report)
                self.create_result()
                return True
        else:
            return False

    def do_calc_single2D(self):
        ''' Gets data from original_data1 and original_data2 and send
            to calculate
        '''
        # Clear current working data and prepare result if needed:
        self.data_for_calculations = []

        # Get data from self.original_data1
        x_data1 = copy.deepcopy(self.original_data1.x)
        y_data1 = copy.deepcopy(self.original_data1.y)
        z_data1 = copy.deepcopy(self.original_data1.z)
        name1 = copy.deepcopy(self.original_data1.name)
        complex1 = copy.deepcopy(self.original_data1.complex)
        datatype1 = copy.deepcopy(self.original_data1.type)
        origin1 = copy.deepcopy(self.original_data1.origin)
        comment1 = copy.deepcopy(self.original_data1.comment)
        parameters1 = copy.deepcopy(self.original_data1.parameters)

        # Extract the data in x and y if needed
        x_data1, y_data1 = self.extract_region_xy(x = x_data1, y = y_data1)
        # Show error if extracted data contains no data
        if y_data1.size == 0:
            Error.show(info = f'For the selected range, the {name1} contains no values')
            self.set_mouse_state(state='')
            return False
        data_1 = {'x':x_data1,
                  'y':y_data1,
                  'z':z_data1,
                  'name':name1,
                  'stk_value':'None',
                  'complex': complex1,
                  'type': datatype1,
                  'origin': origin1,
                  'comment': comment1,
                  'parameters': parameters1
                  }
        self.data_for_calculations.append(data_1)

        if self.use_second:
            # Check if the second selected data is single 2D
            is_2D = self.original_data2.y.ndim == 2
            if self.original_data2.type.lower() != 'single 2D' or is_2D != 2:
                # First is single 2D and second is single 2D
                x_data2 = copy.deepcopy(self.original_data2.x)
                y_data2 = copy.deepcopy(self.original_data2.y)
                z_data2 = copy.deepcopy(self.original_data2.z)
                name2 = copy.deepcopy(self.original_data2.name)
                complex2 = copy.deepcopy(self.original_data1.complex)
                datatype2 = copy.deepcopy(self.original_data1.type)
                origin2 = copy.deepcopy(self.original_data1.origin)
                comment2 = copy.deepcopy(self.original_data1.comment)
                parameters2 = copy.deepcopy(self.original_data1.parameters)

                # Extract the data in x and y
                x_data2, y_data2 = self.extract_region_xy(x=x_data2, y=y_data2)
                data_2 = {'x': x_data2,
                          'y': y_data2,
                          'z':z_data2,
                          'name': name2,
                          'stk_value':'None',
                          'complex': complex2,
                          'type': datatype2,
                          'origin': origin2,
                          'comment': comment2,
                          'parameters': parameters2
                          }
                self.data_for_calculations.append(data_2)
            else:
                Error.show(info='If the first data is 2D, the second must also be 2D, not a stack.', details='')
                return False
        else:
            self.data_for_calculations.append(None)
        # Go to calculate function
        row_to_report = self.calculate()
        # Update data and report
        if isinstance(row_to_report, list):
            if self.report['create']:
                self.add_to_report(row = row_to_report)
                self.create_result()
                self.set_mouse_state(state='')
                return True
        else:
            return False

    def stack_calc(self):
        ''' This method is used if stk_data is calculated as a whole
            using self.calculate_stack method
        '''
        # Clear current working data and prepare result if needed:
        self.data_for_calculations = []

        # Get data from self.original_data1
        x_data1 = copy.deepcopy(self.original_data1.x)
        y_data1 = copy.deepcopy(self.original_data1.y)
        z_data1 = copy.deepcopy(self.original_data1.z)
        name1 = copy.deepcopy(self.original_data1.name) + self.subprog_settings['name_suffix']
        complex1 = copy.deepcopy(self.original_data1.complex)
        datatype1 = copy.deepcopy(self.original_data1.type)
        origin1 = copy.deepcopy(self.original_data1.origin)
        comment1 = copy.deepcopy(self.original_data1.comment)
        parameters1 = copy.deepcopy(self.original_data1.parameters)

        # Extract the data in x and y if needed
        x_data1, y_data1 = self.extract_region_xy(x=x_data1, y=y_data1)
        if y_data1.size == 0:
            Error.show(info=f'For the selected range, the {name1} contains no values')
            self.set_mouse_state(state='')
            self.show_results_matching_first()
            return False
        data_1 = {'x': x_data1,
                  'y': y_data1,
                  'z': z_data1,
                  'name': name1,
                  'stk_value': z_data1,
                  'complex': complex1,
                  'type': datatype1,
                  'origin': origin1,
                  'comment': comment1,
                  'parameters': parameters1
                  }
        self.data_for_calculations.append(data_1)
        if self.use_second:
            # Check if the second selected data is single 2D
            is_2D = self.original_data2.y.ndim == 2
            if self.original_data2.type.lower() != 'single 2D' or is_2D != 2:
                # First is single 2D and second is single 2D
                x_data2 = copy.deepcopy(self.original_data2.x)
                y_data2 = copy.deepcopy(self.original_data2.y)
                z_data2 = copy.deepcopy(self.original_data2.z)
                name2 = copy.deepcopy(self.original_data2.name)
                complex2 = copy.deepcopy(self.original_data1.complex)
                datatype2 = copy.deepcopy(self.original_data1.type)
                origin2 = copy.deepcopy(self.original_data1.origin)
                comment2 = copy.deepcopy(self.original_data1.comment)
                parameters2 = copy.deepcopy(self.original_data1.parameters)

                # Extract the data in x and y
                x_data2, y_data2 = self.extract_region_xy(x=x_data2, y=y_data2)
                if y_data2.size == 0:
                    return False
                try:
                    # Exception called when number of z_data1 is different than z_data2
                    # thus 'stk_value' cannot be created by iteration
                    data_2 = {'x': x_data2,
                              'y': y_data2,
                              'z': z_data2,
                              'name': name2,
                              'stk_value': z_data2,
                              'complex': complex2,
                              'type': datatype2,
                              'origin': origin2,
                              'comment': comment2,
                              'parameters': parameters2
                              }
                except:
                    # Skip setting 'stk_value'
                    data_2 = {'x': x_data2,
                              'y': y_data2,
                              'z': z_data2,
                              'name': name2,
                              'stk_value': '',
                              'complex':complex2,
                              'type': datatype2,
                              'origin': origin2,
                              'comment': comment2,
                              'parameters': parameters2
                    }
                self.data_for_calculations.append(data_2)
            else:
                Error.show(info='If the first data is 2D, the second must also be 2D, not a stack.', details='')
                return False
        else:
            self.data_for_calculations.append(None)
        # Go to calculate function
        row_to_report = self.calculate_stack()
        # Update data and report
        if isinstance(row_to_report, list):
            if self.report['create']:
                self.add_to_report(row=row_to_report)
                self.create_result_stack()
                self.set_mouse_state(state = '')
                return True
        else:
            return False

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
        if y.ndim == 1:
            extracted_y = y[indexes]
        elif y.ndim == 2:
            extracted_y = y[:, indexes]
        else:
            raise ValueError('Extracted_xy method requires y 1D or 2D np.array')
        return extracted_x, extracted_y


    # CREATE, SHOW AND CLEAR REPORTS
    # ------------------------------------------------

    def add_to_report(self, headers = None, row = None):
        ''' Add headers for columns and or additional row to the report'''
        if headers:
            self.report['headers'] = headers
        if row:
            if len(row) != len(self.report['headers']):
                if self.eleana.devel_mode:
                    Error.show(title="Error in report creating.", info="The number of column headers is different than provided columns in row. See console for details")
                    raise ValueError
            else:
                processed_row = []
                for item in row:
                    if item is None:
                        item = ''
                    processed_row.append(item)
                self.report['rows'].append(processed_row)

    def show_report(self):
        ''' Display report as Table a table'''

        if not self.report:
            if self.eleana.devel_mode:
                print("There is no reports in self.report")
            return
        rows = self.report['rows']
        headers = self.report['headers']
        df = pandas.DataFrame(rows, columns=headers)
        default_x = self.report['default_x']
        default_y = self.report['default_y']
        x_unit = self.report['x_unit']
        x_name = self.report['x_name']
        y_name = self.report['y_name']
        y_unit = self.report['y_unit']
        to_group = self.report['to_group']
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
                                group=to_group)
        response = table.get()
        self.update.dataset_list()
        self.update.group_list()
        self.update.all_lists()

    def clear_report(self):
        ''' Clear the created report '''
        self.report['rows'] = []
        self.consecutive_number = 1



    #   UPDATING RESULTS AND GUI
    # ------------------------------------------------

    def show_results_matching_first(self):
        if self.subprog_settings['result']:
            self.app.update.list_in_combobox('sel_result')
            self.app.update.list_in_combobox('r_stk')
            self.app.mainwindow.update()
            first_list = self.app.sel_first._values
            selected_first = self.app.sel_first.get()
            position_in_list = first_list.index(selected_first)
            result_list = self.app.sel_result._values
            result_selected = result_list[position_in_list]
            self.app.result_selected(result_selected)
            self.app.sel_result.set(result_selected)

    def create_result_stack(self):
        ''' Create new result entry in result_dataset when stack is calculated as whole'''
        self.stk_index = -1
        result_create = copy.deepcopy(self.subprog_settings['result'])
        if result_create not in ['add', 'replace']:
            return      # Do nothing if result should not be created

        # Calculate index where spectrum must be inserted:
        results_dataset = self.eleana.results_dataset
        list_of_results = [obj.name for obj in results_dataset]
        new_result = copy.deepcopy(self.original_data1)
        new_result.x = copy.deepcopy(self.data_for_calculations[0]['x'])
        new_result.y = copy.deepcopy(self.data_for_calculations[0]['y'])
        new_result.z = copy.deepcopy(self.data_for_calculations[0]['z'])
        new_result.name = copy.deepcopy(self.data_for_calculations[0]['name'])


        if self.stk_index == -1 and results_dataset:
            results_dataset[-1].x = new_result.x
            results_dataset[-1].y = new_result.y
            results_dataset[-1].z = new_result.z
            name__ = self.app.generate_name_suffix(new_result.name, list_of_results)
            results_dataset[-1].name = name__ + self.subprog_settings['name_suffix']
        elif self.stk_index == -1 and not results_dataset:
            results_dataset.append(new_result)
        self.app.update.list_in_combobox(comboboxID='sel_result')

    def create_result(self):
        ''' Create new result entry in result_dataset '''
        result_create = copy.deepcopy(self.subprog_settings['result'])
        if result_create not in ['add', 'replace']:
            return      # Do nothing if result should not be created

        # Calculate index where spectrum must be inserted:
        results_dataset = self.eleana.results_dataset
        list_of_results = [obj.name for obj in results_dataset]
        new_result = copy.deepcopy(self.original_data1)
        new_result.x = copy.deepcopy(self.data_for_calculations[0]['x'])
        new_result.y = copy.deepcopy(self.data_for_calculations[0]['y'])
        new_result.z = copy.deepcopy(self.data_for_calculations[0]['z'])
        new_result.name = copy.deepcopy(self.data_for_calculations[0]['name'])

        if self.stk_index == -1 and results_dataset:
            results_dataset[-1].x = new_result.x
            results_dataset[-1].y = new_result.y
            results_dataset[-1].z = new_result.z
            name__ = self.app.generate_name_suffix(new_result.name, list_of_results)
            results_dataset[-1].name = name__ + self.subprog_settings['name_suffix']

        elif self.stk_index == -1 and not results_dataset:
            results_dataset.append(new_result)

        elif self.stk_index >= 0:
            index_in_result = len(results_dataset) - 1

            results_dataset[index_in_result].y[self.stk_index] = copy.deepcopy(new_result.y)
        else:
            index_in_result = len(results_dataset) if result_create == 'replace' else max(len(results_dataset) - 1, 0)
        self.app.update.list_in_combobox(comboboxID='sel_result')

    def update_results_list(self, results):
        ''' Puts the created results names into result combobox'''
        if len(self.eleana.results_dataset) == 0:
            self.app.resultFrame.grid_remove()
            return
        self.app.resultFrame.grid()
        self.app.sel_result.configure(values = results)


    #
    # ADDITIONAL METHODS SUCH AS PLACING ANNOTATION IN GRAPH
    # ------------------------------------------------

    def place_annotation(self, x, y = None, which = 'first', style = None):
        ''' Put the annotation at given (x,y) point.
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
        ''' Puts the "value" into the field of CTkEntry defined by "entry" '''
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
        ''' Set cursor to watch or ready for Main GUI and Main Graph'''
        if self.app:
            self.grapher.canvas.get_tk_widget().config(cursor=state)
            self.app.mainwindow.configure(cursor=state)
        return