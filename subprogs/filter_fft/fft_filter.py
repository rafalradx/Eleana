#!/usr/bin/python3
# IMPORT MODULES NEEDED
# -- Here is an example --
import numpy as np
import importlib
import weakref

''' GENERAL SETTINGS '''
# If True all active subprog windows will be closed on start this subprog
CLOSE_SUBPROGS: bool = False

# Folder name containing THIS file
SUBPROG_FOLDER: str = 'filter_fft'

# Name of GUI python file created by pygubu-designer. Usually with ...ui.py endings
GUI_FILE: str = 'fft_filterui.py'

# Name of class in GUI_FILE used to create the window
GUI_CLASS: str = 'FFTFilterUI'

# Title of the window that shown in the main bar
TITLE: str = 'FFT filter'

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
NAME_SUFFIX: str = '_FILTERED'

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
ORIG_IN_ODD_IDX: bool = True

# If both First and Second data are needed set this True
# self.use_second
USE_SECOND: bool = False

# If each subspectrum in a Stack 2D can be processed separately set this to True
# When the calculations requires all data from the stack in x and y set this  to False
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

REPORT_SKIP_FOR_SINGLE:bool = False
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

# Set the maximum number of annotations that can be added to the graph.
# Set to 0 for no limit
# self.subprog_cursor['limit']
CURSOR_LIMIT: int = 0

CURSOR_SNAP: bool = False
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
CURSOR_REQ_TEXT: str = ''

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
class FFTFilter(Methods, WindowGUI):                                                                   #|
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
        ''' This method is called when alif self.app.sel_cursor_mode.get() != "Range select":
            x1, y1 = self.get_selected_points()

        # (2) CALCULATE BASELINE
        if self.interpolate_method == "linear":
            baseline = np.interp(x1_orig, x1, y1, left=None, right=None, period=None)
        elif self.interpolate_method == "linear":
            baseline = np.interp(x1_orig, x1, y1)
        elif self.interpolate_method == "qubic":
            interpolator = CubicSpline(x1, y1)
            baseline = interpolator(x1_orig)
        elif self.interpolate_method == "phip":
            interpolator = PchipInterpolator(x1, y1)
            baseline = interpolator(x1_orig)
        elif self.interpolate_method == "akma":
            interpolator = Akima1DInterpolator(x1, y1)
            baseline = interpolator(x1_orig)
        elif self.interpolate_method == "barycentric":
            interpolator = BarycentricInterpolator(x1, y1)
            baseline = interpolator(x1_orig)


        # Write original data to results
        self.data_for_calculations[0]['x'] = x1_orig
        if self.keep_baseline.get():
            self.data_for_calculations[0]['y'] = baseline
            self.clear_additional_plots()
        else:
            self.data_for_calculations[0]['y'] = y1_orig - baseline
            self.add_to_additional_plots(x=x1_orig, y=baseline, clear=True)

        # Add to additional plots
        #self.clear_additional_plots()
        #self.add_to_additional_plots(x = x1_orig, y = poly_curve, clear=True)
l calculations are finished and main window
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
        self.cutoffFrame = self.builder.get_object('cutoffFrame', self.mainwindow)
        self.remove = self.builder.get_object('remove', self.mainwindow)
        self.remove.grid_remove()

        self.cutoff_box = self.custom_widget(CTkSpinbox(master = self.cutoffFrame, min_value=0, max_value=100000000, step_value=1, command=self.cutoff_changed, scroll_value=1))
        self.cutoff_box.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.switch = self.builder.get_object('switch', self.mainwindow)
        self.switch.select()
        self.lowpass = True

    def low_high_switch(self):
        self.lowpass = bool(self.switch.get())
        if self.lowpass:
            self.switch.configure(text = 'low-pass filter')
        else:
            self.switch.configure(text = 'high-pass filter')
        self.ok_clicked()

    def cutoff_changed(self, value=None):
        try:
            self.freq = float(self.cutoff_box.get())
        except ValueError:
            return
        self.ok_clicked()

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
            z2 = self.data_for_calculations[1+sft]['z']
            name2 = self.data_for_calculations[1+sft]['name']
            stk_value2 = self.data_for_calculations[1+sft]['stk_value']
            complex2 = self.data_for_calculations[1+sft]['complex']
            type2 = self.data_for_calculations[1+sft]['type']
            origin2 = self.data_for_calculations[1+sft]['origin']
            comment2 = self.data_for_calculations[1+sft]['comment']
            parameters2 = self.data_for_calculations[1+sft]['parameters']
        #cursor_positions = self.grapher.cursor_annotations
        # ------------------------------------------

        min = np.min(y1)
        max = np.max(y1)
        n = np.size(y1)
        if n > 0:
            sampling_rate = (max - min) / n
        else:
            return False

        fft_vals = np.fft.fft(y1)
        freqs = np.fft.fftfreq(len(y1), d = sampling_rate)
        if self.lowpass:
            fft_vals[np.abs(freqs) > self.freq] = 0
        else:
            fft_vals[np.abs(freqs) < self.freq] = 0
        self.data_for_calculations[0]['y'] =  np.real(np.fft.ifft(fft_vals))

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
            {'cutoff_box'    : self.cutoff_box.get()    },
            {'switch'        : self.switch.get()}
                ]

    def restore_settings(self):
        val = self.restore('cutoff_box')
        if val:
            self.cutoff_box.set(value = val)
        else:
            self.cutoff_box.set(value = 1)
        self.cutoff_changed()

        val = self.restore('switch')
        if val:
            self.switch.select()
        elif val is None:
            self.switch.select()
        else:
            self.switch.deselect()
        self.low_high_switch()

if __name__ == "__main__":
    tester = TemplateClass()
    pass

