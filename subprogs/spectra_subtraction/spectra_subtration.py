#!/usr/bin/python3
# IMPORT MODULES NEEDED
# -- Here is an example --
from asyncio import set_event_loop_policy
from logging import setLogRecordFactory

import numpy as np
import importlib
from scipy.interpolate import interp1d
from modules.tkdial.tkdial import Dial
from widgets.CTkSpinbox import CTkSpinbox


''' GENERAL SETTINGS '''
# If True all active subprog windows will be closed on start this subprog
CLOSE_SUBPROGS: bool = False

# Folder name containing THIS file
SUBPROG_FOLDER: str = 'spectra_subtraction'

# Name of GUI python file created by pygubu-designer. Usually with ...ui.py endings
GUI_FILE: str = 'spectra_subtractionui.py'

# Name of class in GUI_FILE used to create the window
GUI_CLASS: str = 'SpectraSubtractionUI'

# Title of the window that shown in the main bar
TITLE: str = 'Spectra subtraction'

# If True, this window will be always on top
# self.subprog_settings['on_top']
ON_TOP : bool = True

# If True then values for selected elements will be stored after close
# and restored automatically when subprog is started again.
# This works only until Eleana is closed
RESTORE_SETTINGS = True

# ID name of a CTkLabel widget where the name of current data is displayed.
# CTkLabel with the same ID name must exist in the GUI.
# If not used set this to None
# self.subprog_settings['data_label']
DATA_LABEL: str = None

# The suffix that will be added to the name of processed data.
# For example if "Spectrum" is processed and NAME_SUFFIX = "_MODIFIED"
# you will get "Spectrum_MODIFIED" name in result
# self.subprog_settings['name_suffix']
NAME_SUFFIX: str = ''

# If true, calculations are done automatically upon selection of data in the main GUI
# self.subprog_settings['auto_calculate']
AUTO_CALCULATE: bool = False

''' INPUT DATA CONFIGURATION '''
# Define if data for calculations should be extracted.
# self.regions['from']
#REGIONS_FROM: str = 'none'        # 'none' - do not extract
REGIONS_FROM: str = 'selection'    # 'selection' - take data only from selected range on graph (Range selection)
#REGIONS_FROM: str = 'scale'       # ' scale' - take data from current x scale

# Define if original, not extracted data are added to self.data_for_calculations in indexes +1
# For example. If set True then: self.data_for_calculations[0] = extracted data
#                                self.data_for_calculations[1] = original, not extracted data
# When USE_SECOND is set True then Second data extracted is in [2] and original in [3].
# This is very useful if something must be calculated on selected fragments and then used he results on original data.
# self.regions['orig_in_odd_idx'] <-- this will keep 0 or 1
ORIG_IN_ODD_IDX: bool = False

# If both First and Second data are needed set this True
# self.use_second
USE_SECOND: bool = True

# If each subspectrum in a Stack 2D can be processed separately set this to True
# When the calculations requires all data fro the stack in x and y set this  to False
# If False then the method 'calculate_stack must contain appropriate method
# self.stack_sep
STACK_SEP: bool = True

# If this is True, data containing the parameter 'origin':@result
# will be ignored for calculations.
# This is useful, if 'Group' is set to 'All' and summary data from table
# are added to the dataset. THis prevents taking summary for further calculations.
# self.subprog_settings['result_ignore']
RESULT_IGNORE: bool = True

''' RESULT DATA CONFIGURATION '''
# Define if processed data should be created, added or replaced
# self.subprog_settings['result']
#RESULT_CREATE: str = ''          # Do not create any result dataset
#RESULT_CREATE: str = 'add'      # Add created results to the result_dataset
RESULT_CREATE: str = 'replace'  # Replace the data in result with new results

''' REPORT SETTINGS '''
# Define if a report should be created. Reports contain summary of calculations, values etc.
# self.report['create']
REPORT_CREATE: bool = False

# Results of Stack data usually requires separate calculations for each data in the stack.
# Hence this often requires summary of calculation as a Table.
# If set to True, the summary table will not be shown.
# self.report['report_skip_for_stk']
REPORT_SKIP_FOR_STK: bool = False

# The name of the window containg the reported results.
# self.report['report_window_title']
REPORT_WINDOW_TITLE: str = 'Results'

# Report headers is the list of srtings that contains HEADERS of the table
# in which the results of calculations are shown.
# self.report['headers']
# Here is an example:
REPORT_HEADERS: list = ['Nr',
                  'Name',
                  'X1',
                  'X2',
                  'dX',
                  'Y1',
                  'Y2',
                  'dY']

# Index in REPORT_HEADERS that defines a column to create default X axis.
# This can be manually changed when the report is displayed.
# self.report['default_x']
# Example: 2 means that column 'X1' is taken as default X
REPORT_DEFAULT_X: int = 2

# The same as X but for Y axis.
# self.report['default_y']
# Example: 7 - dY column is set as default Y
REPORT_DEFAULT_Y: int = 7

# The default name of data, that will be used after Add to dataset.
# self.report['report_name']
REPORT_NAME: str = "Report"

# Default name of X axis for report data
# self.report['x_name']
REPORT_NAME_X: str =  'Data Number'

# Default name of Y axis for report data
# self.report['y_name']
REPORT_NAME_Y: str =  'dY Value'

# Default unit name of values in the X axis
# self.report['x_unit']
REPORT_UNIT_X: str = ''

# Default unit name of values in the Y axis
# self.report['y_unit']
REPORT_UNIT_Y: str = ''

# Default name of Group to which the report data are assigned.
# If not existing, the appropriate group is created
# self.report['to_group']
REPORT_TO_GROUP: str = 'RESULT Distance'

''' CURSOR SETTINGS '''
# If False, the manual changing of cursor type in the main GUI Window is disabled.
# self.subprog_cursor['changing']
CURSOR_CHANGING: bool = True

# Name of the cursor that is automatically switched on when the subprog window is opened.
# Possible values: 'None', 'Continuous read XY', 'Selection of points with labels'
#                  'Selection of points', 'Numbered selections', 'Free select', 'Crosshair', 'Range select'
# self.subprog_cursor['type']
CURSOR_TYPE: str = 'None'

# Set the maximum number of annotations that can be added to the graph.
# Set to 0 for no limit
# self.subprog_cursor['limit']
CURSOR_LIMIT: int = 0

# If True the any added cursors in the graph will be removed
# self.subprog_cursor['clear_on_start']
CURSOR_CLEAR_ON_START: bool = False

# Minimum number of cursor annotations needed for calculations.
# Set 0 for no checking
# self.subprog_cursor['cursor_required']
CURSOR_REQUIRED: int = 0

# A text string to show in a pop up window if number of cursors is less than required for calculations
# Leve this empty if no error should be displayed
# self.subprog_cursor['cursor_req_text']
CURSOR_REQ_TEXT: str = 'Please select at least two points.'

# Enable checking if all cursor annotations are between Xmin and Xmax of data_dor_calculations
# self.subprog_cursor['cursor_outside_x']
CURSOR_OUTSIDE_X: bool = False

# The same as for X but for Ymin and Ymax
# self.subprog_cursor['cursor_outside_y']
CURSOR_OUTSIDE_Y: bool = False

# Text to display if any cursor is outside Xmin, Xmax or Ymin, Ymax
# self.subprog_cursor['cursor_outside_text']
CURSOR_OUTSIDE_TEXT: str = 'One or more selected points are outside the (x, y) range of data.'


'''**************************************************************************************************
*                      THE DEFAULT CONSTRUCTOR (LINES BETWEEN **)                                   * 
**************************************************************************************************'''
if __name__ == "__main__":
    module_path = f"subprogs.{SUBPROG_FOLDER}.{GUI_FILE[:-3]}"
    class_name = GUI_CLASS
    from assets.Eleana import Eleana
else:
    module_path = f"{SUBPROG_FOLDER}.{GUI_FILE[:-3]}"
    class_name = GUI_CLASS
mod = importlib.import_module(module_path)
WindowGUI = getattr(mod, class_name)

from subprogs.general_methods.SubprogMethods3 import SubMethods_03 as Methods                       #|
class SpectraSubtraction(Methods, WindowGUI):                                                           #|
    def __init__(self, app=None, which='first', commandline=False):                                 #|
        if app and not commandline:                                                                 #|
            # Initialize window if app is defined and not commandline                               #|
            WindowGUI.__init__(self, app.mainwindow)                                                #|
        # Create settings for the subprog                                                           #|
        self.subprog_settings = {'folder':SUBPROG_FOLDER, 'title': TITLE, 'on_top': ON_TOP, 'data_label': DATA_LABEL, 'name_suffix': NAME_SUFFIX,
                                 'restore':RESTORE_SETTINGS, 'auto_calculate': AUTO_CALCULATE, 'result': RESULT_CREATE, 'result_ignore':RESULT_IGNORE}
        self.regions = {'from': REGIONS_FROM, 'orig_in_odd_idx':int(ORIG_IN_ODD_IDX)}
        self.report = {'nr': 1, 'create': REPORT_CREATE, 'headers': REPORT_HEADERS, 'rows': [], 'x_name': REPORT_NAME_X, 'y_name': REPORT_NAME_Y, 'default_x': REPORT_HEADERS[REPORT_DEFAULT_X], 'default_y': REPORT_HEADERS[REPORT_DEFAULT_Y],
                       'x_unit': REPORT_UNIT_X, 'y_unit': REPORT_UNIT_Y, 'to_group': REPORT_TO_GROUP, 'report_skip_for_stk': REPORT_SKIP_FOR_STK, 'report_window_title': REPORT_WINDOW_TITLE, 'report_name': REPORT_NAME}
        self.subprog_cursor = {'type': CURSOR_TYPE, 'changing': CURSOR_CHANGING, 'limit': CURSOR_LIMIT, 'clear_on_start': CURSOR_CLEAR_ON_START, 'cursor_required': CURSOR_REQUIRED, 'cursor_req_text':CURSOR_REQ_TEXT,
                               'cursor_outside_x':CURSOR_OUTSIDE_X, 'cursor_outside_y':CURSOR_OUTSIDE_Y, 'cursor_outside_text':CURSOR_OUTSIDE_TEXT}
        self.use_second = USE_SECOND                                                                #|
        self.stack_sep = STACK_SEP                                                                  #|
        Methods.__init__(self, app=app, which=which, commandline=commandline, close_subprogs=CLOSE_SUBPROGS)


    # PRE-DEFINED FUNCTIONS TO EXECUTE AT DIFFERENT STAGES OF SUBPROG METHODS
    # Unused definitions can be deleted

    def graph_action(self, variable=None, value=None):
        ''' Do something when cursor action on is triggered. '''

    def after_data_changed(self, variable, value):
        ''' This method is called after data changing by clicking in the Main GUI. '''

    def after_calculations(self):
        ''' This method is called after single calculations
            and just before showing the report. '''

    def after_result_show_on_graph(self):
        ''' This method is called immediately when results
            for graph are ready but grapher canva has not been refreshed yet. '''

    def after_ok_clicked(self):
        ''' This method is called when all functions are
            finished after clicking 'Calculate' button. '''

    def after_process_group_clicked(self):
        ''' This method is called when all functions are
             finished after clicking 'Process group' button. '''

    def after_graph_plot(self):
        ''' This method is called when the main application refreshes Graph canva content.
            For example, after changing First data, the graph is reploted and then
            this function is run.
            DO NOT USE FUNCTIONS USING GRAPHER METHODS HERE!'''

    def finish_action(self, by_method):
        ''' This method is called when all calculations are finished and main window
            awaits for action. This is useful if you need to put annotations to the graph etc.
            by_method - the name of a method that triggered the action.
        '''


    # DEFINE YOUR CUSTOM METHODS FOR THIS ROUTINE
    # ----------------------------------------------
    def configure_window(self):
        # HERE DEFINE ADDITIONAL MAIN WINDOW CONFIGURATION
        #self.mainwindow =

        # HERE DEFINE YOUR REFERENCES TO WIDGETS
        from widgets.CTkSpinbox import CTkSpinbox

        self.data_frame = self.builder.get_object('ctkframe4', self.mainwindow)
        self.data_frame.grid_remove()

        self.encoder1frame = self.builder.get_object('encoder1frame', self.mainwindow)
        self.encoder1 = Dial(master = self.encoder1frame, command=self.parameters_changed)
        self.encoder1.grid(row = 0, column=0, sticky="nsew")
        self.encoder2frame = self.builder.get_object('encoder2frame', self.mainwindow)
        self.encoder2 = Dial(master=self.encoder2frame,  command=self.parameters_changed)
        self.encoder2.grid(row=0, column=0, sticky="nsew")
        self.encoder3frame = self.builder.get_object('encoder3frame', self.mainwindow)
        self.encoder3 = Dial(master=self.encoder3frame,  command=self.parameters_changed)
        self.encoder3.grid(row=0, column=0, sticky="nsew")
        self.spinbox1frame = self.builder.get_object('spinbox1frame', self.mainwindow)
        self.spinbox1frame.grid_columnconfigure(0, weight=1)
        self.spinbox1 = CTkSpinbox(master = self.spinbox1frame, logarithm_step = True, disable_wheel = True, min_value = 1e-20, max_value = 1e+20, start_value = 1,  command=self.parameters_changed)
        self.spinbox1.grid(row = 0, column = 0, sticky = 'nsew')

        self.spinbox2frame = self.builder.get_object('spinbox2frame', self.mainwindow)
        self.spinbox2frame.grid_columnconfigure(0, weight=1)
        self.spinbox2 = CTkSpinbox(master=self.spinbox2frame, logarithm_step = True, disable_wheel = True, min_value = 1e-20, max_value = 1e+20, start_value = 1,  command=self.parameters_changed)
        self.spinbox2.grid(row=0, column=0, sticky='nsew')
        self.spinbox3frame = self.builder.get_object('spinbox3frame', self.mainwindow)
        self.spinbox3frame.grid_columnconfigure(0, weight=1)
        self.spinbox3 = CTkSpinbox(master=self.spinbox3frame, logarithm_step = True, disable_wheel = True, min_value = 1e-20, max_value = 1e+20, start_value = 1,  command=self.parameters_changed)
        self.spinbox3.grid(row=0, column=0, sticky='nsew')

        # Entry Boxes
        self.multiply_y_by = self.builder.get_object("ctkentry1", self.mainwindow)
        self.shift_y_by = self.builder.get_object("ctkentry2", self.mainwindow)
        self.shift_x_by =   self.builder.get_object("ctkentry3", self.mainwindow)

        # Set validation for Entry boxes
        self.set_validation_for_ctkentries(list_of_entries = [self.multiply_y_by, self.shift_y_by, self.shift_x_by])

        # Settings comboboxes
        self.sel_operation_mode = self.builder.get_object("ctkcombobox4", self.mainwindow)
        self.sel_interpolation = self.builder.get_object("ctkcombobox1", self.mainwindow)
        self.sel_alignment_interval = self.builder.get_object("ctkcombobox2", self.mainwindow)
        self.sel_resampling_interval = self.builder.get_object("ctkcombobox3", self.mainwindow)

        self.values = {}

    def parameters_changed(self, selection=None):
        ''' After manual modification of knob or spinbox '''
        self.calculate_values()
        self.update_entries()
        #self.ok_clicked()

    def odejmij_widma_auto(self, X1, Y1, X2, Y2, method='auto', spline_order=3, fill_value=0.0):
        """
        Interpoluje Y2 do X1 i odejmuje od Y1.
        Parametry:
        ----------
        X1, Y1 : ndarray – dane widma bazowego
        X2, Y2 : ndarray – dane widma do interpolacji
        metoda : str – 'auto', 'linear', 'spline'
        stopień_spline : int – stopień splajnu (1=liniowy, 3=kubiczny itd.)
        fill_value : float – wartość poza zakresem X2

        Zwraca:
        -------
        X1, Y_roznica : ndarray – siatka i widmo różnicowe
        """

        # Set method
        if method == 'auto':
            if len(X2) < 50 or spline_order == 1:
                method_final = 'linear'
            else:
                method_final = 'spline'
        else:
            method_final = method

        # Interpolate
        if method_final == 'linear':
            Y2_interp = np.interp(X1, X2, Y2, left=fill_value, right=fill_value)
        elif method_final == 'spline':
            spline = InterpolatedUnivariateSpline(X2, Y2, k=spline_order)
            Y2_interp = spline(X1)
        else:
            raise ValueError("Invalid interoplation method. Use: 'auto', 'linear' or 'spline'")
        Y_difference = Y1 - Y2_interp
        return X1, Y_difference

    def calculate_stack(self, commandline = False):
        ''' If STACK_SEP is False it means that data in stack should
            not be treated as separate data but are calculated as whole

            DO NOT USE FUNCTION REQUIRED GUI UPDATE HERE
            '''

        # AVAILABLE DATA. REMOVE UNNECESSARY
        # EACH X,Y,Z IS NP.ARRAY
        # X, Z is 1D, Y is 2D
        # -----------------------------------------
        sft = +self.regions['orig_in_odd_idx']
        x1 = self.data_for_calculations[0]['x']
        y1 = self.data_for_calculations[0]['y']
        z1 = self.data_for_calculations[0]['z']
        name1 = self.data_for_calculations[0]['name']
        stk_value1 = self.data_for_calculations[0]['stk_value']
        complex1 = self.data_for_calculations[0]['complex']
        type1 = self.data_for_calculations[0]['type']
        origin1 = self.data_for_calculations[0]['origin']
        comment1 = self.data_for_calculations[0]['comment']
        parameters1 = self.data_for_calculations[0]['parameters']
        if self.use_second:
            x2 = self.data_for_calculations[1]['x']
            y2 = self.data_for_calculations[1]['y']
            z2 = self.data_for_calculations[1]['z']
            name2 = self.data_for_calculations[1]['name']
            stk_value2 = self.data_for_calculations[1]['stk_value']
            complex2 = self.data_for_calculations[1]['complex']
            type2 = self.data_for_calculations[1]['type']
            origin2 = self.data_for_calculations[1]['origin']
            comment2 = self.data_for_calculations[1]['comment']
            parameters2 = self.data_for_calculations[1]['parameters']
        # ------------------------------------------

    def calculate(self, commandline = False):
        ''' The algorithm for calculations on single x,y,z data.

        Usage:
            x1, y1, z1: contain the prepared x, y, z data for calculations
            x2, y2, z2: contain the reference data to use for example to subtract from data1
        After calculation put calculated data to:
            x1, y1 and z1 etc.
            result: the value of resulted calculations

            DO NOT USE FUNCTION REQUIRED GUI UPDATE HERE
        '''

        # AVAILABLE DATA. REMOVE UNNECESSARY
        # EACH X,Y,Z IS NP.ARRAY OF ONE DIMENSION
        # -----------------------------------------
        sft = +self.regions['orig_in_odd_idx']
        x1 = self.data_for_calculations[0]['x']
        y1 = self.data_for_calculations[0]['y']
        z1 = self.data_for_calculations[0]['z']
        name1 = self.data_for_calculations[0]['name']
        stk_value1 = self.data_for_calculations[0]['stk_value']
        complex1 = self.data_for_calculations[0]['complex']
        type1 = self.data_for_calculations[0]['type']
        origin1 = self.data_for_calculations[0]['origin']
        comment1 = self.data_for_calculations[0]['comment']
        parameters1 = self.data_for_calculations[0]['parameters']
        if self.use_second:
            x2 = self.data_for_calculations[1+sft]['x']
            y2 = self.data_for_calculations[1+sft]['y']
            z2 = self.data_for_calculations[1]+sft['z']
            name2 = self.data_for_calculations[1+sft]['name']
            stk_value2 = self.data_for_calculations[1+sft]['stk_value']
            complex2 = self.data_for_calculations[1+sft]['complex']
            type2 = self.data_for_calculations[1+sft]['type']
            origin2 = self.data_for_calculations[1+sft]['origin']
            comment2 = self.data_for_calculations[1+sft]['comment']
            parameters2 = self.data_for_calculations[1+sft]['parameters']
        cursor_positions = self.grapher.cursor_annotations
        # ------------------------------------------

        self.data_for_calculations[0]['y'] = self.pseudomodulation(x = x1,
                                             y = y1,
                                             mod_amp=self.modulation,
                                             harmonic=self.harmonic,
                                             normalize=self.normalize)

        # Send calculated values to result (if needed). This will be sent to command line
        result = None # <--- HERE IS THE RESULT TO SEND TO COMMAND LINE

        # Create summary row to add to the report. The values must match the column names in REPORT_HEADERS
        row_to_report = None

        return row_to_report

    def calculate_values(self):
        mutliply_y = float(self.encoder1.get()) * float(self.spinbox1.get())
        shift_y = float(self.encoder2.get()) * float(self.spinbox2.get())
        shift_x = float(self.encoder3.get()) * float(self.spinbox3.get())
        self.values = {'multiply_y' : mutliply_y,
                       'shift_y' : shift_y,
                       'shift_x' : shift_x
                       }

    def update_entries(self):
        self.set_entry_value(entry = self.multiply_y_by,
                             value = self.values['multiply_y'])
        self.set_entry_value(entry=self.shift_y_by,
                             value=self.values['shift_y'])
        self.set_entry_value(entry=self.shift_x_by,
                             value=self.values['shift_x'])

    def save_settings(self):
        ''' Stores required values to self.eleana.subprog_storage
            This is stored in memory only, not in disk
            define each list element as:
            {'key_for_storage' : function_for_getting_value()}
        '''
        return  [
            {'encoder1'     : self.encoder1.get()   },
            {'encoder2'     : self.encoder2.get()   },
            {'encoder3'     : self.encoder3.get()   },
            {'spinbox1'     : self.spinbox1.get()   },
            {'spinbox2'     : self.spinbox2.get()   },
            {'spinbox3'     : self.spinbox3.get()   },
            {'sel_operation_mode'   :   self.sel_operation_mode.get()},
            {'sel_interpolation'    :   self.sel_interpolation.get()},
            {'sel_alignment_interval':  self.sel_alignment_interval.get()},
            {'sel_resampling_interval':  self.sel_resampling_interval.get()}
                ]

    def restore_settings(self):
        val = self.restore('encoder1')
        if val:
            self.encoder1.set(value = val)
        else:
            self.encoder1.set(value = 1)

        val = self.restore('encoder2')
        if val:
            self.encoder2.set(value=val)
        else:
            self.encoder2.set(value=0)

        val = self.restore('encoder3')
        if val:
            self.encoder3.set(value=val)
        else:
            self.encoder3.set(value=0)

        val = self.restore('spinbox1')
        if val:
            self.spinbox1.set(value = val)
        else:
            self.spinbox1.set(value = 1)

        val = self.restore('spinbox2')
        if val:
            self.spinbox2.set(value=val)
        else:
            self.spinbox2.set(value=1)

        val = self.restore('spinbox3')
        if val:
            self.spinbox3.set(value=val)
        else:
            self.spinbox3.set(value=1)

        val = self.restore('sel_operation_mode')
        if val:
            self.sel_operation_mode.set(value=val)
        else:
            self.sel_operation_mode.set(value = 'Subtraction (First - Second')

        val = self.restore('sel_interpolation')
        if val:
            self.sel_interpolation.set(value=val)
        else:
            self.sel_interpolation.set(value='linear')

        val = self.restore('sel_alignment_interval')
        if val:
            self.sel_alignment_interval.set(value=val)
        else:
            self.sel_alignment_interval.set(value='Common')

        val = self.restore('sel_resampling_interval')
        if val:
            self.sel_resampling_interval.set(value=val)
        else:
            self.sel_resampling_interval.set(value='Lower')

        self.calculate_values()
        self.update_entries()

if __name__ == "__main__":
    tester = TemplateClass()
    pass

