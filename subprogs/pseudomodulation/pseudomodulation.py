#!/usr/bin/python3
# IMPORT MODULES NEEDED
# -- Here is an example --

import numpy as np
import importlib
import scipy.signal
import weakref

''' GENERAL SETTINGS '''
# If True all active subprog windows will be closed on start this subprog
CLOSE_SUBPROGS: bool = False

# Folder name containing THIS file
SUBPROG_FOLDER: str = 'pseudomodulation'

# Name of GUI python file created by pygubu-designer. Usually with ...ui.py endings
GUI_FILE: str = 'pseudomodulationui.py'

# Name of class in GUI_FILE used to create the window
GUI_CLASS: str = 'PseudomodulationUI'

# Title of the window that shown in the main bar
TITLE: str = 'Pseudomodulation'

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
DATA_LABEL: str = 'data_label'

# The suffix that will be added to the name of processed data.
# For example if "Spectrum" is processed and NAME_SUFFIX = "_MODIFIED"
# you will get "Spectrum_MODIFIED" name in result
# self.subprog_settings['name_suffix']
NAME_SUFFIX: str = '_PSMOD'

# If true, calculations are done automatically upon selection of data in the main GUI
# self.subprog_settings['auto_calculate']
AUTO_CALCULATE: bool = False

''' INPUT DATA CONFIGURATION '''
# Define if data for calculations should be extracted.
# self.regions['from']
REGIONS_FROM: str = 'none'        # 'none' - do not extract
#REGIONS_FROM: str = 'selection'    # 'selection' - take data only from selected range on graph (Range selection)
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
USE_SECOND: bool = False

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

REPORT_SKIP_FOR_SINGLE = False
# The name of the window containg the reported results.
# self.report['report_window_title']
REPORT_WINDOW_TITLE: str = 'Results of distance measurements'

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
REPORT_NAME: str = "Distance measurements"

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

CURSOR_SNAP = False
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

from subprogs.general_methods.SubprogMethods5 import SubMethods_05 as Methods                       #|
class PseudoModulation(Methods, WindowGUI):                                                           #|
    def __init__(self, app=None, which='first', commandline=False):
        self.__app = weakref.ref(app)
        if app and not commandline:
            # Initialize window if app is defined and not commandline
            WindowGUI.__init__(self, self.__app().mainwindow)
        # Create settings for the subprog                                                           #|
        self.subprog_settings = {'folder': SUBPROG_FOLDER, 'title': TITLE, 'on_top': ON_TOP, 'data_label': DATA_LABEL,
                                 'name_suffix': NAME_SUFFIX,
                                 'auto_calculate': AUTO_CALCULATE, 'result': RESULT_CREATE,
                                 'result_ignore': RESULT_IGNORE,
                                 'restore': RESTORE_SETTINGS}
        self.regions = {'from': REGIONS_FROM, 'orig_in_odd_idx': ORIG_IN_ODD_IDX}

        self.report = {'nr': 1, 'create': REPORT_CREATE, 'headers': REPORT_HEADERS, 'rows': [], 'x_name': REPORT_NAME_X,
                       'y_name': REPORT_NAME_Y, 'default_x': REPORT_HEADERS[REPORT_DEFAULT_X],
                       'default_y': REPORT_HEADERS[REPORT_DEFAULT_Y],
                       'x_unit': REPORT_UNIT_X, 'y_unit': REPORT_UNIT_Y, 'to_group': REPORT_TO_GROUP,
                       'report_skip_for_stk': REPORT_SKIP_FOR_STK, 'report_window_title': REPORT_WINDOW_TITLE,
                       'report_name': REPORT_NAME,
                       'report_skip_for_single': REPORT_SKIP_FOR_SINGLE}

        self.subprog_cursor = {'type': CURSOR_TYPE, 'changing': CURSOR_CHANGING, 'limit': CURSOR_LIMIT,
                               'clear_on_start': CURSOR_CLEAR_ON_START, 'cursor_required': CURSOR_REQUIRED,
                               'cursor_req_text': CURSOR_REQ_TEXT,
                               'cursor_outside_x': CURSOR_OUTSIDE_X, 'cursor_outside_y': CURSOR_OUTSIDE_Y,
                               'cursor_outside_text': CURSOR_OUTSIDE_TEXT,
                               'snap_to': CURSOR_SNAP}
        self.use_second = USE_SECOND  # |
        self.stack_sep = STACK_SEP
        Methods.__init__(self, app_weak=self.__app, which=which, commandline=commandline, close_subprogs=CLOSE_SUBPROGS)
        self.mainwindow.protocol('WM_DELETE_WINDOW', self.cancel)

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
        self.harmFrame = self.builder.get_object('harmFrame', self.mainwindow)
        self.modFrame = self.builder.get_object('modFrame', self.mainwindow)
        self.entry1 = self.builder.get_object('ctkentry1', self.mainwindow)
        self.entry2 = self.builder.get_object('ctkentry2', self.mainwindow)
        self.entry1.grid_remove()
        self.entry2.grid_remove()

        self.harm_box = self.custom_widget(CTkSpinbox(master=self.harmFrame, min_value=0, max_value=2, step_value=1,  command=self.parameters_changed, scroll_value = 1))
        self.harm_box.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.mod_box = self.custom_widget(CTkSpinbox(master=self.modFrame, min_value=0, max_value=10000, step_value=0.1, command = self.parameters_changed, scroll_value = 1))
        self.mod_box.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.normalize_box = self.builder.get_object('normalize', self.mainwindow)

    def parameters_changed(self, selection=None):
        self.harmonic = int(self.harm_box.get())
        self.modulation = float(self.mod_box.get())
        self.normalize = bool(self.normalize_box.get())
        self.ok_clicked()

    def pseudomodulation(self,x, y, mod_amp, harmonic=0, normalize=False):
        """
        Simulated pseudomodulation for EPR data for different harmonics.
        Parameters:
            x (np.array): the x axis of the spectrum
            yb(np.array): the amplitude of EPR signal.
            mod_amp (float): modulation amplitude in unit of x axis.
            harmonic (int): number of harmonic (0, 1, 2).
            normalize (bool): normalize to amplitude to input signal?
        Returns:
            np.array: pseudomodulation array
        """
        dx = x[1] - x[0]
        signal = y
        shift_points = int(np.round(mod_amp / dx))
        n = len(signal)
        if shift_points >= n // 2:
            raise ValueError("Modulation is too large in relation to the signal")
        # Shifts
        plus = np.roll(signal, -shift_points)
        minus = np.roll(signal, shift_points)
        plus[-shift_points:] = 0
        minus[:shift_points] = 0
        # Modulation by harmonic number
        if harmonic == 0:
            window_width = 2 * shift_points + 1
            kernel = np.ones(window_width) / window_width
            modulated = scipy.signal.convolve(signal, kernel, mode='same')
        elif harmonic == 1:
            modulated = plus - minus
        elif harmonic == 2:
            modulated = plus - 2 * signal + minus
        else:
            raise ValueError("Wrong harmonic number. It should be 0, 1, 2.")
        # Normalize amplitude
        if normalize:
            orig_amp = np.max(np.abs(signal))
            mod_amp = np.max(np.abs(modulated))
            if mod_amp > 0:
                modulated *= (orig_amp / mod_amp)
        return modulated

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
        #cursor_positions = self.grapher.cursor_annotations
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

    def save_settings(self):
        ''' Stores required values to self.eleana.subprog_storage
            This is stored in memory only, not in disk
            define each list element as:
            {'key_for_storage' : function_for_getting_value()}
        '''
        return  [
            {'harm_box'    : self.harm_box.get()    },
            {'mod_box'     : self.mod_box.get()     },
            {'normalize'   : self.normalize_box.get() }
                ]

    def restore_settings(self):
        val = self.restore('harm_box')
        if val:
            self.harm_box.set(value = val)
        else:
            self.harm_box.set(value = 0)

        val = self.restore('mod_box')
        if val:
            self.mod_box.set(value = val)
        else:
            self.mod_box.set(value = 1)
        val = self.restore('normalize')
        if val == True:
            self.normalize_box.select()
        else:
            self.normalize_box.deselect()
        self.parameters_changed()


if __name__ == "__main__":
    tester = TemplateClass()
    pass

