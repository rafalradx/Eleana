from assets.Observer import Observer
import copy
import numpy as np
from assets.Error import Error
from subprogs.table.table import CreateFromTable
import pandas
import matplotlib.pyplot as plt
from pathlib import Path
from functools import wraps

'''
======================================================
==                                                  ==
==            SUBPROG METHODS VERSION               ==
==                       3                          ==
==                                                  ==
====================================================== 
'''

def check_busy(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.eleana.busy:
            if self.eleana.devel_mode:
                print(f"{Path(__file__).name}, {method.__name__}: self.eleana.busy = True")
            return  # Breaks a method execution
        return method(self, *args, **kwargs)  # Go to a method
    return wrapper


class SubMethods_03:
    def __init__(self, app=None, which='first', commandline=False, close_subprogs=False):
        self.subprog_storage_data = []
        self.commandline = commandline
        self.general_error_skip = False
        self.update_gui = True
        self.data_for_calculations = []
        self.consecutive_number = 1
        self.additional_plots_settings = {
            'color': 'gray',
            'linewidth': 2,
            'linestyle': 'dashed',
        }

        if app and not self.commandline:
            # Window start from Menu in GUI
            self.app = app
            self.mainwindow.protocol('WM_DELETE_WINDOW', self.cancel)
            self.master = self.app.mainwindow
            self.eleana = self.app.eleana
            self.eleana.active_subprog = self
            self.grapher = self.app.grapher
            self.update = self.app.update
            self.mainwindow.title(self.subprog_settings['title'])
            self.mainwindow.attributes('-topmost', self.subprog_settings['on_top'])

            # Close all previous subprogs
            if close_subprogs:
                self.app.close_all_subprogs()

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
            if cursor_type != 'none' or cursor_type != '':
                # Configure cursor
                self.subprog_cursor['previous'] = copy.copy(self.grapher.current_cursor_mode['label'])
                self.grapher.cursor_limit = self.subprog_cursor['limit']
                self.app.sel_cursor_mode.set(self.subprog_cursor['type'])
                self.app.sel_graph_cursor(self.subprog_cursor['type'])
                self.app.mainwindow.update()
                if not self.subprog_cursor['changing']:
                    # Disable cursor changing
                    self.app.sel_cursor_mode.configure(state="disabled")
                if self.subprog_cursor['clear_on_start']:
                    # Clear current cursors
                    if self.subprog_cursor['type'].lower() == 'range select':
                        self.grapher.clear_selected_ranges()
                    else:
                        self.grapher.clear_all_annotations()
            # Restore settings for the subporg
            self.subprog_id = self.subprog_settings['folder'] + "|" + self.subprog_settings['title']
            if self.subprog_settings['restore']:
                self.restore_settings()

    # STANDARD METHODS FOR MAIN APPLICATION
    # ----------------------------------------------

    def get(self):
        ''' Returns self.response to the main application after close '''
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event=None):
        ''' Close the window with self.response = None '''
        # Store settings
        if self.subprog_settings['restore']:
             self.save_storage_on_close()

        self.response = None
        # Return cursor selection to enabled
        self.app.sel_cursor_mode.configure(state="normal")
        self.app.sel_cursor_mode.set(self.subprog_cursor['previous'])
        self.app.sel_graph_cursor(self.subprog_cursor['previous'])
        # Unregister observer
        self.eleana.detach(self.observer)
        self.grapher.clear_selected_ranges()
        self.clear_additional_plots()
        self.mainwindow.destroy()
        self.eleana.active_subprog = None
        self.grapher.plot_graph()
        self.eleana.busy = False

        # Excecute additional code in subprog
        self.after_quit_subprog()

    # GETTING THE DATA ACCORDING TO ELEANA.SELECTION
    # ----------------------------------------------

    def get_data(self, group_processing = False, variable=None, value=None):
        ''' Makes a copy of the selected data and stores it in self.original_data.
            You may perform calculations on self.original_data. '''
        index = self.eleana.selections[self.which]
        if index < 0:
            return False
        parameters = self.eleana.dataset[index].parameters
        origin = parameters.get('origin', None)
        if self.eleana.selections[self.which] >= 0:  # If selection is not None
            ignore = self.subprog_settings.get('result_ignore', True)
            if origin == "@result" and ignore:
                return False
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
            if value is None:
                try:
                    self.grapher.clear_all_annotations()
                except:
                    if self.eleana.devel_mode:
                        print("Subprogmethods2.data_changed() - Clear all annotations failed")
            self.after_data_changed(variable=variable, value=value)
            return False
        elif variable == 'f_stk' or variable == 's_stk':
            self.app.mainwindow.configure(cursor="")
            self.grapher.canvas.get_tk_widget().config(cursor="")
            try:
                self.grapher.clear_all_annotations()
            except:
                if self.eleana.devel_mode:
                    print("Subprogmethods2.data_changed() - Clear all annotations failed")
            self.after_data_changed(variable=variable, value=value)
            return False
        elif variable == 'grapher_action' and value == 'range_start':
            self.app.mainwindow.configure(cursor="")
            self.grapher.canvas.get_tk_widget().config(cursor="")
            return False
        elif variable == 'grapher_action' and value == 'range_end':
            self.app.mainwindow.configure(cursor="")
            self.grapher.canvas.get_tk_widget().config(cursor="")
            return False
        elif variable == 'grapher_action' and value == 'plot':
            self.after_graph_plot()
            return False
        elif variable == "grapher_action":
            return False
        elif variable == 'result':
            self.after_data_changed(variable=variable, value=value)
            return False
        else:
            self.after_data_changed(variable=variable, value=value)
        if self.subprog_settings['auto_calculate']:
            self.ok_clicked()
        return True

    # STANDARD METHODS FOR SUBPROG GUI BUTTONS
    # -------------------------------------------------

    def ok_clicked(self):
        ''' [-OK-] button
            This is standard function in SubprogMethods '''
        if self.eleana.busy:
            if self.eleana.devel_mode:
                print('ok_clicked - blocked by self.eleana.busy')
            return
        self.eleana.busy = True
        #self.app.mainwindow.configure(cursor='watch')
        try:
            self.start_single_calculations()
        except Exception as e:
            Error.show(info = e)
        #self.set_mouse_state(state='')
        del self.data_for_calculations
        del self.original_data1
        del self.original_data2

        self.eleana.busy = False
        self.after_ok_clicked()
        self.show_results_matching_first()

    def process_group_clicked(self):
        ''' [-Process Group-] button
            This is standard function in SubprogMethods '''
        if self.eleana.busy:
            if self.eleana.devel_mode:
                print('process_group_clicked - blocked by self.eleana.busy')
            return
        self.eleana.busy = True
        self.set_mouse_state(state='watch')

        try:
            self.perform_group_calculations()
        except Exception as e:
            Error.show(info = e)
        self.show_results_matching_first()
        self.set_mouse_state(state='')
        self.eleana.busy = False
        self.after_process_group_clicked()
        del self.data_for_calculations
        del self.original_data1
        del self.original_data2
        self.show_results_matching_first()

    def show_report_clicked(self):
        ''' [-Show Report-] button
            This is standard function in SubprogMethods '''
        if self.eleana.busy:
            if self.eleana.devel_mode:
                print('show_report_clicked - blocked by self.eleana.busy')
            return
        self.eleana.busy = True
        self.set_mouse_state(state='')
        self.show_report()
        self.eleana.busy = False

    def clear_report_clicked(self):
        ''' [-Show Report-] button
            This is standard function in SubprogMethods '''
        if self.eleana.busy:
            if self.eleana.devel_mode:
                print('clear_report_clicked - blocked by self.eleana.busy')
            return
        self.clear_report()

    # TRIGGERING CALCULATIONS
    # -----------------------------------------------

    def start_single_calculations(self):
        ''' This function is triggered by clicking "Calculate" button'''
        required_cursors = self.subprog_cursor['cursor_required']
        nr_of_annotations = len(self.grapher.cursor_annotations)
        if required_cursors > nr_of_annotations:
            if self.subprog_cursor['cursor_req_text']:
                Error.show(title='', info=self.subprog_cursor['cursor_req_text'])
            return False
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
        #self.set_mouse_state("watch")
        # Create result_dataset if add or replace is set
        if self.subprog_settings['result'] == 'add':
            # Simply add the result to the eleana.results_dataset
            self.result_data = copy.deepcopy(self.original_data1)

            # Extract data from selections:
            # Only if ORIG_IN_ODD_IDX is False.
            if not self.regions['orig_in_odd_idx']:
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
            self.result_data.name = self.result_data.name + self.subprog_settings['name_suffix']
            if len(self.eleana.results_dataset) == 0:
                # Results_dataset is empty so new_result must be added
                self.result_data = copy.deepcopy(self.original_data1)

                # Extract data from selections:
                if not self.regions['orig_in_odd_idx']:
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
                status = self.stack_calc()  # Prepare the whole stack for calculations
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
                        if group_processing == False:
                            self.app.mainwindow.update()
                    status = self.do_calc_stk_data()
                    if status:
                        self.consecutive_number += 1
                        self.stk_index += 1
                    else:
                        return status
                # After stk calculations
                self.stk_index = -1
                #self.set_mouse_state("")
                skip_report_show = self.report.get('report_skip_for_stk', False)

        # Single data that is not a stack
        elif self.original_data1.type.lower() == 'single 2D' or not is_2D:
            self.stk_index = -1
            if self.data_label is not None:
                self.data_label.configure(text=self.original_data1.name_nr)
                if group_processing == False:
                    self.app.mainwindow.update()
            status = self.do_calc_single2D()
            if status:
                self.consecutive_number += 1
            else:
                return status
            skip_report_show = True
            if group_processing == False:
                self.show_results_matching_first()

        else:
            Error.show(info='The type of the selected data cannot be determined. Please define the "type" parameter.',
                       details='')

        if group_processing:
            # If group processing is activated skip GUI update
            return True
        else:
            if len(self.eleana.results_dataset) == 0:
                self.after_calculations()
                self.show_report()
                return True
            else:
                # Select result to the last entry
                list_of_results = self.app.sel_result._values
                selected_value_text = list_of_results[-1]
                self.app.result_selected(selected_value_text)
                self.app.sel_result.set(selected_value_text)
        if not skip_report_show:
            self.after_calculations()
            self.show_report()
        return True

    def perform_group_calculations(self):
        required_cursors = self.subprog_cursor['cursor_required']
        nr_of_annotations = len(self.grapher.cursor_annotations)
        if required_cursors > nr_of_annotations:
            if self.subprog_cursor['cursor_req_text']:
                Error.show(title='', info=self.subprog_cursor['cursor_req_text'])
            return False

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
        if self.subprog_settings['result'] == 'replace':
            self.subprog_settings['result'] = 'add'

        # Do the single calculation for the each of the data in the
        for each in group_list:
            self.eleana.selections['first'] = each
            status1 = self.get_data(group_processing = True)
            if status1:
                status2 = self.perform_single_calculations(group_processing=True)
                if not status2:
                    self.eleana.selections = copy_selections
                    self.subprog_settings = copy_of_subprog_settings
                    #self.show_results_matching_first()
                    self.after_result_show_on_graph()
                    return False

        # After processing
        self.eleana.selections = copy_selections
        self.subprog_settings = copy_of_subprog_settings

        # Display result settings that match selection in first
        self.show_results_matching_first()
        self.after_result_show_on_graph()

        # Show Report
        self.after_calculations()
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
            self.after_result_show_on_graph()
            return False
        data_1 = {'x': x_data1,
                  'y': y_data1,
                  'z': z_data1,
                  'name': name1,
                  'stk_value': z_data1[self.stk_index],
                  'complex': complex1,
                  'type': datatype1,
                  'origin': origin1,
                  'comment': comment1,
                  'parameters': parameters1
                  }
        self.data_for_calculations.append(data_1)

        # Add non extracted data if ORIG_IN_ODD_IDX is True
        if self.regions['orig_in_odd_idx']:
            x_data1_orig = copy.deepcopy(self.original_data1.x)
            y_data1_orig = copy.deepcopy(self.original_data1.y[self.stk_index])
            z_data1_orig = copy.deepcopy(self.original_data1.z)
            data_1_orig =   {'x': x_data1_orig,
                              'y': y_data1_orig,
                              'z': z_data1_orig,
                              'name': name1,
                              'stk_value': copy.deepcopy(z_data1[self.stk_index]),
                              'complex': copy.deepcopy(complex1),
                              'type': copy.deepcopy(datatype1),
                              'origin': copy.deepcopy(origin1),
                              'comment': copy.deepcopy(comment1),
                              'parameters': copy.deepcopy(parameters1)
                              }
            self.data_for_calculations.append(data_1_orig)

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
                              'stk_value': copy.deepcopy(z_data2[self.stk_index]),
                              'complex': copy.deepcopy(complex2),
                              'type': copy.deepcopy(datatype2),
                              'origin': copy.deepcopy(origin2),
                              'comment': copy.deepcopy(comment2),
                              'parameters': copy.deepcopy(parameters2)
                              }
                except:
                    # Skip setting 'stk_value'
                    data_2 = {'x': x_data2,
                              'y': y_data2,
                              'z': z_data2,
                              'name': name2,
                              'stk_value': '',
                              'complex': complex2,
                              'type': datatype2,
                              'origin': origin2,
                              'comment': comment2,
                              'parameters': parameters2
                              }
                self.data_for_calculations.append(data_2)

                # Add original data
                if self.regions['orig_in_odd_idx']:
                    x_data2_orig = copy.deepcopy(self.original_data2.x)
                    y_data2_orig = copy.deepcopy(self.original_data2.y[self.stk_index])
                    z_data2_orig = copy.deepcopy(self.original_data2.z)
                    data_2_orig = {'x': x_data2_orig,
                                   'y': y_data2_orig,
                                   'z': z_data2_orig,
                                   'name': name2,
                                   'stk_value': z_data2[self.stk_index],
                                   'complex': complex2,
                                   'type': datatype2,
                                   'origin': origin2,
                                   'comment': comment2,
                                   'parameters': parameters2
                                   }
                    self.data_for_calculations.append(data_2_orig)
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

    def do_calc_single2D(self):
        ''' Gets data from original_data1 and original_data2 and send
            to calculate
        '''
        # Clear current working data and prepare result if needed:
        self.data_for_calculations = []

        # Get data from self.original_data1
        x_data1 = self.original_data1.x.copy()
        y_data1 = self.original_data1.y.copy()
        z_data1 = copy(self.original_data1.z)

        name1 = self.original_data1.name.copy()
        complex1 = self.original_data1.complex.copy()
        datatype1 = self.original_data1.type.copy()
        origin1 = self.original_data1.origin.copy()
        comment1 = self.original_data1.comment.copy()
        parameters1 = self.original_data1.parameters.copy()

        # Extract the data in x and y if needed
        x_data1, y_data1 = self.extract_region_xy(x=x_data1, y=y_data1)

        # Show error if extracted data contains no data
        if y_data1.size == 0:
            Error.show(info=f'The {name1} contains no values for the selected range or the current cursor position.')
            self.set_mouse_state(state='')
            return False
        data_1 = {'x': x_data1,
                  'y': y_data1,
                  'z': z_data1,
                  'name': name1,
                  'stk_value': 'None',
                  'complex': complex1,
                  'type': datatype1,
                  'origin': origin1,
                  'comment': comment1,
                  'parameters': parameters1
                  }
        self.data_for_calculations.append(data_1)

        # Add non extracted data if ORIG_IN_ODD_IDX is True
        if self.regions['orig_in_odd_idx']:
            x_data1_orig = self.original_data1.x.copy()
            y_data1_orig = self.original_data1.y.copy()
            z_data1_orig = self.original_data1.z.copy()
            data_1_orig = {'x': x_data1_orig,
                           'y': y_data1_orig,
                           'z': z_data1_orig,
                           'name': name1,
                           'stk_value': 'None',
                           'complex': complex1,
                           'type': datatype1,
                           'origin': origin1,
                           'comment': comment1,
                           'parameters': parameters1
                           }
            self.data_for_calculations.append(data_1_orig)

        if self.use_second:
            # Check if the second selected data is single 2D
            is_2D = self.original_data2.y.ndim == 2
            if self.original_data2.type.lower() != 'single 2D' or is_2D != 2:
                # First is single 2D and second is single 2D
                x_data2 = self.original_data2.x.copy()
                y_data2 = self.original_data2.y.copy()
                z_data2 = self.original_data2.z.copy()

                name2 = self.original_data2.name.copy()
                complex2 = self.original_data1.complex.copy()
                datatype2 = self.original_data1.type.copy()
                origin2 = self.original_data1.origin.copy()
                comment2 = self.original_data1.comment.copy()
                parameters2 = self.original_data1.parameters.copy()

                # Extract the data in x and y
                x_data2, y_data2 = self.extract_region_xy(x=x_data2, y=y_data2)
                data_2 = {'x': x_data2,
                          'y': y_data2,
                          'z': z_data2,
                          'name': name2,
                          'stk_value': 'None',
                          'complex': complex2,
                          'type': datatype2,
                          'origin': origin2,
                          'comment': comment2,
                          'parameters': parameters2
                          }
                self.data_for_calculations.append(data_2)

                # Add original data
                if self.regions['orig_in_odd_idx']:
                    x_data2_orig = self.original_data2.x.copy()
                    y_data2_orig = self.original_data2.y[self.stk_index].copy()
                    z_data2_orig = self.original_data2.z.copy()
                    data_2_orig = {'x': x_data2_orig,
                                   'y': y_data2_orig,
                                   'z': z_data2_orig,
                                   'name': name2,
                                   'stk_value': z_data2[self.stk_index],
                                   'complex': complex2,
                                   'type': datatype2,
                                   'origin': origin2,
                                   'comment': comment2,
                                   'parameters': parameters2
                                   }
                    self.data_for_calculations.append(data_2_orig)

            else:
                Error.show(info='If the first data is 2D, the second must also be 2D, not a stack.', details='')
                return False
        else:
            self.data_for_calculations.append(None)

        # Go to calculate function
        row_to_report = self.calculate()
        # Check if cursors are within (x,y) of x_data1 and y_data1
        status = self.check_cursor_bounds(x=x_data1, y=y_data1)
        if not status:
            if self.subprog_cursor['cursor_outside_text']:
                Error.show(title=name1, info=self.subprog_cursor['cursor_outside_text'])
            return False

        if isinstance(row_to_report, list):
            if self.report['create']:
                self.add_to_report(row=row_to_report)
        self.create_result()
        #self.set_mouse_state(state='')
        return True

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
            self.after_result_show_on_graph()
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

        # Add non extracted data if ORIG_IN_ODD_IDX is True
        if self.regions['orig_in_odd_idx']:
            x_data1_orig = copy.deepcopy(self.original_data1.x)
            y_data1_orig = copy.deepcopy(self.original_data1.y)
            z_data1_orig = copy.deepcopy(self.original_data1.z)
            data_1_orig = {'x': x_data1_orig,
                           'y': y_data1_orig,
                           'z': z_data1_orig,
                           'name': name1,
                           'stk_value': 'None',
                           'complex': complex1,
                           'type': datatype1,
                           'origin': origin1,
                           'comment': comment1,
                           'parameters': parameters1
                           }
            self.data_for_calculations.append(data_1_orig)

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
                              'complex': complex2,
                              'type': datatype2,
                              'origin': origin2,
                              'comment': comment2,
                              'parameters': parameters2
                              }
                self.data_for_calculations.append(data_2)

                # Add non extracted data if ORIG_IN_ODD_IDX is True
                if self.regions['orig_in_odd_idx']:
                    x_data1_orig = copy.deepcopy(self.original_data1.x)
                    y_data1_orig = copy.deepcopy(self.original_data1.y)
                    z_data1_orig = copy.deepcopy(self.original_data1.z)
                    data_1_orig = {'x': x_data1_orig,
                                   'y': y_data1_orig,
                                   'z': z_data1_orig,
                                   'name': name1,
                                   'stk_value': 'None',
                                   'complex': complex1,
                                   'type': datatype1,
                                   'origin': origin1,
                                   'comment': comment1,
                                   'parameters': parameters1
                                   }
                    self.data_for_calculations.append(data_1_orig)

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
        self.stk_index = -1
        self.create_result()
        del self.data_for_calculations
        return True

    def extract_region_xy(self, x, y):
        ''' Extract data using selected range (self.grapher.color_span) or scale (x_min, x_max) from array in x,y '''
        if self.regions['from'] == 'scale':
            ranges = [self.grapher.ax.get_xlim()]
        elif self.regions['from'] == 'selection':
            ranges = self.eleana.color_span['ranges']
        elif self.regions['from'] == 'none':
            return x, y
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

    def add_to_report(self, headers=None, row=None):
        ''' Add headers for columns and or additional row to the report'''
        if headers:
            self.report['headers'] = headers
        if row:
            if len(row) != len(self.report['headers']):
                if self.eleana.devel_mode:
                    Error.show(title="Error in report creating.",
                               info="The number of column headers is different than provided columns in row. See console for details")
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

        if not self.report['create']:
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
        window_title = self.report['report_window_title']
        name = self.report['report_name']
        table = CreateFromTable(window_title=window_title,
                                eleana_app=self.eleana,
                                master=self.mainwindow,
                                df=df,
                                name=name,
                                default_x_axis=default_x,
                                default_y_axis=default_y,
                                x_unit=x_unit,
                                x_name=x_name,
                                y_unit=y_unit,
                                y_name=y_name,
                                group=to_group,
                                set_parameters={'origin': '@result'})
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
            try:
                result_selected = result_list[position_in_list]
            except IndexError:
                result_selected = result_list[-1]
            self.app.result_selected(result_selected)
            self.app.sel_result.set(result_selected)
        self.after_result_show_on_graph()

    def create_result_stack(self):
        ''' Create new result entry in result_dataset when stack is calculated as whole'''
        self.stk_index = -1
        result_create = copy.deepcopy(self.subprog_settings['result'])
        if result_create not in ['add', 'replace']:
            return  # Do nothing if result should not be created

        # Calculate index where spectrum must be inserted:
        results_dataset = self.eleana.results_dataset
        list_of_results = [obj.name for obj in results_dataset]
        new_result = copy.deepcopy(self.original_data1)
        new_result.x = copy.deepcopy(self.data_for_calculations[0]['x'])
        new_result.y = copy.deepcopy(self.data_for_calculations[0]['y'])
        new_result.z = copy.deepcopy(self.data_for_calculations[0]['z'])
        new_result.name = copy.deepcopy(self.data_for_calculations[0]['name'])
        new_result.complex = copy.deepcopy(self.data_for_calculations[0]['complex'])
        new_result.type = copy.deepcopy(self.data_for_calculations[0]['type'])
        new_result.origin = copy.deepcopy(self.data_for_calculations[0]['origin'])
        new_result.comment = copy.deepcopy(self.data_for_calculations[0]['comment'])
        new_result.parameters = copy.deepcopy(self.data_for_calculations[0]['parameters'])

        if self.stk_index == -1 and results_dataset:
            results_dataset[-1].x = new_result.x
            results_dataset[-1].y = new_result.y
            results_dataset[-1].z = new_result.z
            name__ = self.app.generate_name_suffix(new_result.name, list_of_results)
            results_dataset[-1].name = name__ + self.subprog_settings['name_suffix']
            results_dataset[-1].complex = new_result.complex
            results_dataset[-1].type = new_result.type
            results_dataset[-1].origin = new_result.origin
            results_dataset[-1].parameters = new_result.parameters
            results_dataset[-1].comment = new_result.comment
        elif self.stk_index == -1 and not results_dataset:
            results_dataset.append(new_result)
        self.app.update.list_in_combobox(comboboxID='sel_result')

    def create_result(self):
        ''' Create new result entry in result_dataset '''
        result_create = copy.deepcopy(self.subprog_settings['result'])
        if result_create not in ['add', 'replace']:
            return  # Do nothing if result should not be created

        # Calculate index where spectrum must be inserted:
        results_dataset = self.eleana.results_dataset
        list_of_results = [obj.name for obj in results_dataset]
        new_result = copy.deepcopy(self.original_data1)
        new_result.x = copy.deepcopy(self.data_for_calculations[0]['x'])
        new_result.y = copy.deepcopy(self.data_for_calculations[0]['y'])
        new_result.z = copy.deepcopy(self.data_for_calculations[0]['z'])
        new_result.name = copy.deepcopy(self.data_for_calculations[0]['name'])
        new_result.complex = copy.deepcopy(self.data_for_calculations[0]['complex'])
        new_result.type = copy.deepcopy(self.data_for_calculations[0]['type'])
        new_result.origin = copy.deepcopy(self.data_for_calculations[0]['origin'])
        new_result.comment = copy.deepcopy(self.data_for_calculations[0]['comment'])
        new_result.parameters = copy.deepcopy(self.data_for_calculations[0]['parameters'])

        if self.stk_index == -1 and results_dataset:
            results_dataset[-1].x = new_result.x
            results_dataset[-1].y = new_result.y
            results_dataset[-1].z = new_result.z
            name__ = self.app.generate_name_suffix(new_result.name, list_of_results)
            results_dataset[-1].name = name__ + self.subprog_settings['name_suffix']
            results_dataset[-1].complex = new_result.complex
            results_dataset[-1].type = new_result.type
            results_dataset[-1].origin = new_result.origin
            results_dataset[-1].parameters = new_result.parameters
            results_dataset[-1].comment = new_result.comment

        elif self.stk_index == -1 and not results_dataset:
            results_dataset.append(new_result)

        elif self.stk_index >= 0:
            index_in_result = len(results_dataset) - 1
            if self.stk_index <= len(results_dataset[index_in_result].y) - 1:
                results_dataset[index_in_result].y[self.stk_index] = copy.deepcopy(new_result.y)

            else:
                results_dataset[index_in_result].x = copy.deepcopy(new_result.x)
                results_dataset[index_in_result].z = copy.deepcopy(new_result.z)
                results_dataset[index_in_result].complex = copy.deepcopy(new_result.complex)
                results_dataset[index_in_result].type = copy.deepcopy(new_result.type)
                results_dataset[index_in_result].origin = copy.deepcopy(new_result.origin)
                results_dataset[index_in_result].comment = copy.deepcopy(new_result.comment)
                results_dataset[index_in_result].parameters = copy.deepcopy(new_result.parameters)
        self.app.update.list_in_combobox(comboboxID='sel_result')
        return

    def update_results_list(self, results):
        ''' Puts the created results names into result combobox'''
        if len(self.eleana.results_dataset) == 0:
            self.app.resultFrame.grid_remove()
            return
        self.app.resultFrame.grid()
        self.app.sel_result.configure(values=results)

    def add_to_additional_plots(self, x, y, label = None, style = None, clear = False):
        ''' This adds additional plots to the grapher
            for example showing baseline or fits, etc.
            The settings for the plot are taken from
            self.additional_plots_settings
        '''
        if clear:
            self.grapher.additional_plots = []
        if style is None:
            style = self.additional_plots_settings
        if np.size(x) != np.size(y) and not self.subprog_settings['ignore_dimensions']:
            Error.show(master = self.mainwindow, info = f"X and Y have different dimensions.")
            return
        data = {'label':label, 'x':x, 'y':y, 'style': style}
        self.grapher.additional_plots.append(data)

    def clear_additional_plots(self):
        self.grapher.additional_plots = []

    # ADDITIONAL METHODS FOR CHECKING CURSOR POSITIONS ON GRAPH
    # ------------------------------------------------

    def check_cursor_bounds(self, x, y):
        ''' If CURSOR_OUTSIDE_X or Y is set then check if cursor
            at (x,y) is within the range of selected data'''
        outside_x = self.subprog_cursor['cursor_outside_x']
        outside_y = self.subprog_cursor['cursor_outside_y']
        if outside_x and outside_y:
            in_bounds = self.all_cursors_within_bounds(x=x, y=y)
        elif outside_x and not outside_y:
            in_bounds = self.all_cursors_within_bounds(x=x, y=None)
        elif outside_y and not outside_x:
            in_bounds = self.all_cursors_within_bounds(x=None, y=y)
        else:
            return True
        answer = all(in_bounds)
        return answer

    def all_cursors_within_bounds(self, x=None, y=None):
        answers = []
        for cursor in self.grapher.cursor_annotations:
            answer = self.is_cursors_within_bounds(cursor=cursor, x=x, y=y)
            answers.append(answer)
        return answers

    def is_cursors_within_bounds(self, cursor, x=None, y=None):
        cursor_x = cursor['point'][0]
        cursor_y = cursor['point'][1]
        if x is not None:
            if x.size == 0:
                x_in_range = False
            else:
                x_in_range = (cursor_x >= x.min()) & (cursor_x <= x.max())
        else:
            x_in_range = True
        if y is not None:
            if y.size == 0:
                y_in_range = False
            else:
                y_in_range = (cursor_y >= y.min()) & (cursor_y <= y.max())
        else:
            y_in_range = True
        return x_in_range and y_in_range

    # METHODS FOR CUSTOM CURSOR HANDLING
    # ------------------------------------------------
    def get_selected_points(self):
        ''' Returns unique x and y data for selected points '''
        if self.grapher.cursor_annotations:
            x = []
            y = []
            for selection in self.grapher.cursor_annotations:
                nxt_x = selection['point'][0]
                nxt_y = selection['point'][1]
                if nxt_x not in x:
                    x.append(nxt_x)
                    y.append(nxt_y)
        else:
            return None, None
        return x, y

    def clear_custom_annotations_list(self):
        ''' Clear the list of added custom_annotations'''
        self.eleana.custom_annotations = []
        try:
            self.grapher.annotationlist.delete("all")
        except:
            pass

    def place_custom_annotation(self, x, y=None, which='first', refresh_gui=True):
        ''' Puts the annotation at given (x,y) point.
            If only x is set the y coordinate will snap to the curve indicated in "which" variable.
            If x and y are set then the annotation will appear at given (x,y) coordinates
            '''
        if x is None:
            return
        if y:
            snap = False
        else:
            snap = True
        self.set_custom_annotation(point=(x, y), snap=snap, which=which)
        annots = self.eleana.custom_annotations
        i = 0
        for annot in annots:
            xy = annot['point']
            number_ = str(i + 1) if self.grapher.style_of_annotation['number'] else ''
            # self.grapher.ax.annotate(text=self.grapher.style_of_annotation['text'] + number_,
            #                  xy=xy, arrowprops=self.grapher.style_of_annotation['arrowprops']
            #                  )
            self.grapher.ax.annotate(text=self.grapher.style_of_annotation['text'] + number_,
                                     xy=xy,
                                     xytext=self.grapher.xytext_position(xy),
                                     arrowprops=self.grapher.style_of_annotation['arrowprops'],
                                     bbox=self.grapher.style_of_annotation['bbox'],
                                     fontsize=self.grapher.style_of_annotation['fontsize'],
                                     color=self.grapher.style_of_annotation['color']
                                     )

            i += 1
        self.grapher.canvas.draw()

    def remove_custom_annotations_from_graph(self):
        ''' Remove all annotations added to the graph '''
        for child in self.grapher.ax.get_children():
            if isinstance(child, plt.Annotation):
                child.remove()
        self.grapher.canvas.draw()

    def set_custom_annotation(self, point, snap=True, which='first'):
        ''' Create annotation programmatically at the specified (x, y) point. '''

        def _find_nearest_index(x_data, x_coord):
            x_data = np.array(x_data)
            index = np.abs(x_data - x_coord).argmin()
            return index

        x_coord, y_coord = point  # Unpack the point coordinates
        if which == 'first':
            nr = 0
            stk_index = self.eleana.selections['f_stk']
        elif which == 'second':
            nr = 1
            stk_index = self.eleana.selections['s_stk']
        else:
            nr = 2
            stk_index = self.eleana.selections['r_stk']
        lines = self.grapher.ax.get_lines()
        line = lines[nr]
        curve_name = line.get_label()
        index = self.eleana.get_index_by_name(selected_value_text=curve_name)
        x_data, y_data = line.get_data()
        if snap:
            index_of_x = _find_nearest_index(x_data, x_coord)
            y_coord = y_data[index_of_x]
            x_coord = x_data[index_of_x]
        else:
            y_coord = point[1]
            x_coord = point[0]
        number_ = len(self.eleana.custom_annotations)
        custom_annot = {'type': None,
                        'curve': curve_name,
                        'index': index,
                        'stk_index': stk_index,
                        'point': (x_coord, y_coord),
                        'nr': number_}
        self.eleana.custom_annotations.append(custom_annot)
        self.grapher.cursor_annotations.append(custom_annot)
        self.add_custom_annotation_entry(custom_annot)

    def add_custom_annotation_entry(self, annotation):
        ''' Creates the entry and adds it to the annotation list'''
        nr = annotation['nr']
        curve = annotation['curve']
        point_x = annotation['point'][0]
        point_y = annotation['point'][1]
        if nr < 10:
            nr = '#0' + str(nr)
        else:
            nr = '#' + str(nr)
        entry = nr + ' | ' + str(curve) + ' (' + str(round(point_x, 2)) + ', ' + str(round(point_y, 2)) + ')'
        self.grapher.annotationlist.insert("END", entry)

    # METHODS FOR CTKENTRIES SUCH AS VALIDATION
    # -------------------------------------------

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
            entry.configure(state='normal')
            entry.delete(0, 'end')
            entry.insert(0, str(value))
            entry.configure(state='disabled')
        else:
            entry.delete(0, 'end')
            entry.insert(0, str(value))

    def set_mouse_state(self, state=""):
        ''' Set cursor to watch or ready for Main GUI and Main Graph'''
        self.mainwindow.configure(cursor=state)
        if self.app:
            self.grapher.canvas.get_tk_widget().config(cursor=state)
            self.app.mainwindow.configure(cursor=state)
        return


    # STORE AND RESTORE SETTINGS
    # -------------------------------------------------
    def to_store(self, to_save: dict):
        ''' Create entry for each storage values.
        '''

        if self.subprog_settings['restore']:
            self.subprog_storage_data.append(to_save)
        else:
            if self.eleana.devel_mode:
                print('SubprogMethods3:store, if RESTORE is False or to_save parameter is None')

    def save_storage_on_close(self):
        ''' Create entry for all subprog storge values in
            self.eleana.subprog_storage
        '''
        elements = self.save_settings()
        for element in elements:
            self.to_store(element)
        storage = copy.deepcopy(self.subprog_storage_data)
        self.eleana.subprog_storage[self.subprog_id] = storage

    def restore(self, element):
        ''' Get data from self.eleana.subprog_storage
            for widget and returns stored values
        '''
        subprog_field = self.eleana.subprog_storage.get(self.subprog_id, None)
        if subprog_field is None:
            return None
        to_restore = next(line[element] for line in subprog_field if element in line)
        return to_restore

    # DECORATORS FOR ERROR HANDLING
    # -------------------------------------------------

    @staticmethod
    def skip_if_empty_graph(func):
        ''' This method skips the decorated function if there is no data in the graph.'''

        def wrapper(*args, **kwargs):
            # Take class instance
            instance = args[0]
            # Take data from self.grapher
            x_data, y_data = instance.grapher.get_graph_line(index=0)
            if x_data is None or y_data is None:
                return None
            elif x_data.size == 0 or y_data.size == 0:
                return None
            # Go to original function
            return func(*args, **kwargs)

        return wrapper

    def after_gui_clicked(self, widget):
        ''' This is called when all actions are finished after clicking GUI buttons
            widget - contains the name of method that triggered this method
            '''

    # DUMMY FUNCTIONS TO OVERRIDE BY SUBPROG
    # ------------------------------------------------

    def after_data_changed(self, variable, value):
        return

    def after_calculations(self):
        return

    def after_result_show_on_graph(self):
        return

    def after_ok_clicked(self):
        return

    def after_process_group_clicked(self):
        return

    def after_graph_plot(self):
        return

    def graph_action(self, variable=None, value=None):
        return

    def finish_action(self, by_method):
        return

    def after_quit_subprog(self):
        return