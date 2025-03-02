#!/usr/bin/python3
# IMPORT MODULES NEEDED
# -- Here is an example --
import numpy as np
from pathlib import Path


''' GENERAL SETTINGS '''
# If True all active subprog windows will be closed on start this subprog
CLOSE_SUBPROGS = False

# Folder name containing THIS file
SUBPROG_FOLDER = 'distance_read'

# Name of GUI python file created by pygubu-designer. Usually with ...ui.py endings
GUI_FILE = 'DistanceReadui.py'

# Name of class in GUI_FILE used to create the window
GUI_CLASS = 'DistanceReadUI'

# Title of the window that shown in the main bar
TITLE = 'Calculate XY Distance'

# If True, this window will be always on top
# self.subprog_settings['on_top']
ON_TOP = True

# ID name of a CTkLabel widget where the name of current data is displayed.
# CTkLabel with the same ID name must exist in the GUI.
# If not used set this to None
# self.subprog_settings['data_label']
DATA_LABEL = 'data_label'

# The suffix that will be added to the name of processed data.
# For example if "Spectrum" is processed and NAME_SUFFIX = "_MODIFIED"
# you will get "Spectrum_MODIFIED" name in result
# self.subprog_settings['name_suffix']
NAME_SUFFIX = ''

# If true, calculations are done automatically upon selection of data in the main GUI
# self.subprog_settings['auto_calculate']
AUTO_CALCULATE = False

''' INPUT DATA CONFIGURATION '''
# Define if data for calculations should be extracted.
# self.regions['from']
REGIONS_FROM = 'none'         # 'none' - do not extract
#REGIONS_FROM = 'selection'   # 'selection' - take data only from selected range on graph (Range selection)
#REGIONS_FROM = 'scale'       # ' scale' - take data from current x scale

# If both First and Second data are needed set this True
# self.use_second
USE_SECOND = False

# If each subspectrum in a Stack 2D can be processed separately set this True
# When the calculations requires all data in x and y set this False
# If False then the method 'calculate_stack must contain appropriate method
# self.stack_sep
STACK_SEP = True

# If this is True, data containing the parameter 'origin':@result
# will be ignored for calculations.
# This is useful, if 'Group' is set to 'All' and summary data from table
# are added to the dataset. THis prevents taking summary for further calculations.
# self.subprog_settings['result_ignore']
RESULT_IGNORE = True

''' RESULT DATA CONFIGURATION '''
# Define if processed data should be created, added or replaced
# self.subprog_settings['result']
RESULT_CREATE = ''          # Do not create any result dataset
#RESULT_CREATE = 'add'      # Add created results to the result_dataset
#RESULT_CREATE = 'replace'  # Replace the data in result with new results

''' REPORT SETTINGS '''
# Define if a report should be created. Reports contain summary of calculations, values etc.
# self.report['create']
REPORT_CREATE = True

# Results of Stack data usually requires separate calculations for each data in the stack.
# Hence this often requires summary of calculation as a Table.
# If set to True, the summary table will not be shown.
# self.report['report_skip_for_stk']
REPORT_SKIP_FOR_STK = False

# The name of the window containg the reported results.
# self.report['report_window_title']
REPORT_WINDOW_TITLE = 'Results of distance measurements'

# Report headers is the list of srtings that contains HEADERS of the table
# in which the results of calculations are shown.
# self.report['headers']
# Here is an example:
REPORT_HEADERS = ['Nr',
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
REPORT_DEFAULT_X = 2

# The same as X but for Y axis.
# self.report['default_y']
# Example: 7 - dY column is set as default Y
REPORT_DEFAULT_Y = 7

# The default name of data, that will be used after Add to dataset.
# self.report['report_name']
REPORT_NAME = "Distance measurements"

# Default name of X axis for report data
# self.report['x_name']
REPORT_NAME_X =  'Data Number'

# Default name of Y axis for report data
# self.report['y_name']
REPORT_NAME_Y =  'dY Value'

# Default unit name of values in the X axis
# self.report['x_unit']
REPORT_UNIT_X = ''

# Default unit name of values in the Y axis
# self.report['y_unit']
REPORT_UNIT_Y = ''

# Default name of Group to which the report data are assigned.
# If not existing, the appropriate group is created
# self.report['to_group']
REPORT_TO_GROUP = 'RESULT Distance'

''' CURSOR SETTINGS '''
# If False, the manual changing of cursor type in the main GUI Window is disabled.
# self.subprog_cursor['changing']
CURSOR_CHANGING = False

# Name of the cursor that is automatically switched on when the subprog window is opened.
# Possible values: 'None', 'Continuous read XY', 'Selection of points with labels'
#                  'Selection of points', 'Numbered selections', 'Free select', 'Crosshair', 'Range select'
# self.subprog_cursor['type']
CURSOR_TYPE = 'Free select'

# Set the maximum number of annotations that can be added to the graph.
# Set to 0 for no limit
# self.subprog_cursor['limit']
CURSOR_LIMIT = 0

# If True the any added cursors in the graph will be removed
# self.subprog_cursor['clear_on_start']
CURSOR_CLEAR_ON_START = True

# Minimum number of cursor annotations needed for calculations.
# Set 0 for no checking
# self.subprog_cursor['cursor_required']
CURSOR_REQUIRED = 2

# A text string to show in a pop up window if number of cursors is less than required for calculations
# Leve this empty if no error should be displayed
# self.subprog_cursor['cursor_req_text']
CURSOR_REQ_TEXT = 'Please select two points.'

# Enable checking if all cursor annotations are between Xmin and Xmax of data_dor_calculations
# self.subprog_cursor['cursor_outside_x']
CURSOR_OUTSIDE_X = False

# The same as for X but for Ymin and Ymax
# self.subprog_cursor['cursor_outside_y']
CURSOR_OUTSIDE_Y = False

# Text to display if any cursor is outside Xmin, Xmax or Ymin, Ymax
# self.subprog_cursor['cursor_outside_text']
CURSOR_OUTSIDE_TEXT = 'One or more selected points are outside the (x, y) range of data.'


'''**************************************************************************************************
*                      THE DEFAULT CONSTRUCTOR (LINES BETWEEEN **)                                  * 
**************************************************************************************************'''
if __name__ == "__main__":                                                                          #|
    #current_dir = Path(__file__).resolve().parent.name
    cmd_to_import = 'from subprogs.general_methods.Testui import TestUI as WindowGUI'
else:                                                                                               #|
    cmd_to_import = f'from {SUBPROG_FOLDER}.{GUI_FILE[:-3]} import {GUI_CLASS} as WindowGUI'        #|
exec(cmd_to_import)                                                                                 #|
from subprogs.general_methods.SubprogMethods3 import SubMethods_03 as Methods                       #|
class TemplateClass(Methods, WindowGUI):                                                            #|
    def __init__(self, app=None, which='first', commandline=False):                                 #|
        if app and not commandline:                                                                 #|
            # Initialize window if app is defined and not commandline                               #|
            WindowGUI.__init__(self, app.mainwindow)                                                #|
        # Create settings for the subprog                                                           #|
        self.subprog_settings = {'title': TITLE, 'on_top': ON_TOP, 'data_label': DATA_LABEL, 'name_suffix': NAME_SUFFIX, 'auto_calculate': AUTO_CALCULATE, 'result': RESULT_CREATE, 'result_ignore':RESULT_IGNORE}
        self.regions = {'from': REGIONS_FROM}
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
        if self.keep_track:
            self.find_minmax_clicked()
        else:
           self.clear_custom_annotations_list()
           self.remove_custom_annotations_from_graph()


    # DEFINE YOUR CUSTOM METHODS FOR THIS ROUTINE
    # ----------------------------------------------
    def configure_window(self):
        # HERE DEFINE ADDITIONAL MAIN WINDOW CONFIGURATION
        #self.mainwindow =

        # HERE DEFINE YOUR REFERENCES TO WIDGETS
        self.x1_entry = self.builder.get_object('x1_entry', self.mainwindow)
        self.x2_entry = self.builder.get_object('x2_entry', self.mainwindow)
        self.dx_entry = self.builder.get_object('dx_entry', self.mainwindow)
        self.y1_entry = self.builder.get_object('y1_entry', self.mainwindow)
        self.y2_entry = self.builder.get_object('y2_entry', self.mainwindow)
        self.dy_entry = self.builder.get_object('dy_entry', self.mainwindow)
        self.check_keep_track = self.builder.get_object('check_track_minmax', self.mainwindow)
        self.keep_track = False
        self.btn_findminmax = self.builder.get_object('btn_findminmax', self.mainwindow)

        # Binding to Return/Enter after changing CTkEntries content
        self.x1_entry.bind("<Return>",      lambda event: self.entry_value_changed(event, id="x1"))
        self.x1_entry.bind("<KP_Enter>",    lambda event: self.entry_value_changed(event, id="x1"))
        self.x2_entry.bind("<Return>",      lambda event: self.entry_value_changed(event, id="x2"))
        self.x2_entry.bind("<KP_Enter>",    lambda event: self.entry_value_changed(event, id="x2"))

        # Define list of CTkEntries that should be validated for floats
        self.set_validation_for_ctkentries([
                self.x1_entry,
                self.x2_entry,
                self.y1_entry,
                self.y2_entry
                ])

        # Set disabled field
        self.dx_entry.configure(state='disabled')
        self.dy_entry.configure(state='disabled')

    def entry_value_changed(self, event, id):
        x1 = self.x1_entry.get()
        x2 = self.x2_entry.get()
        if x1 and x2:
            x1 =float(x1)
            x2 = float(x2)
            self.clear_custom_annotations_list()
            self.remove_custom_annotations_from_graph()
            self.place_custom_annotation(x=x1)
            self.place_custom_annotation(x=x2)

    @Methods.skip_if_empty_graph
    def find_minmax_clicked(self):
        self.btn_findminmax.configure(state="disabled")
        x_data, y_data = self.grapher.get_graph_line(index = 0)
        index_min_y = np.argmin(y_data)
        min_x = x_data[index_min_y]
        min_y = y_data[index_min_y]
        index_max_y = np.argmax(y_data)
        max_x = x_data[index_max_y]
        max_y = y_data[index_max_y]
        dx = max_x - min_x
        dy = max_y - min_y

        self.set_entry_value(entry = self.x1_entry, value=min_x)
        self.set_entry_value(entry = self.x2_entry, value=max_x)
        self.set_entry_value(entry=self.y1_entry, value=min_y)
        self.set_entry_value(entry=self.y2_entry, value=max_y)
        self.set_entry_value(entry=self.dy_entry, value=dy)
        self.set_entry_value(entry=self.dx_entry, value=dx)

        self.clear_custom_annotations_list()
        self.remove_custom_annotations_from_graph()
        self.place_custom_annotation(x = min_x)
        self.place_custom_annotation(x = max_x)
        self.btn_findminmax.configure(state="normal")
        return True

    def track_minmax_clicked(self):
        self.keep_track = self.check_keep_track.get()
        if self.keep_track:
            self.find_minmax_clicked()

    def calculate_stack(self, commandline = False):
        ''' If STACK_SEP is False it means that data in stack should
            not be treated as separate data but are calculated as whole

            DO NOT USE FUNCTION REQUIRED GUI UPDATE HERE
            '''
        # AVAILABLE DATA. REMOVE UNNECESSARY
        # EACH X,Y,Z IS NP.ARRAY
        # X, Z is 1D, Y is 2D
        # -----------------------------------------
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
        cursor_positions = self.grapher.cursor_annotations
        # ------------------------------------------

        if self.keep_track:
            # Auto detect maximum and minimum using numpy
            index_min_y = np.argmin(y1)
            min_x = x1[index_min_y]
            min_y = y1[index_min_y]
            index_max_y = np.argmax(y1)
            max_x = x1[index_max_y]
            max_y = y1[index_max_y]
            minimum = [min_x, min_y]
            maximum = [max_x, max_y]
        else:
            # Do not detect where maximum and minimum are
            p1 = cursor_positions[0]
            p2 = cursor_positions[1]
            minimum = ([p1['point'][0], p1['point'][1]])
            maximum = ([p2['point'][0], p2['point'][1]])

        # Get x1 and x2
        x1val = minimum[0]
        x2val = maximum[0]

        # Find index in x_data which is closest to x1 or x2
        if x1val < x1.min() or x1val > x1.max():
            return False
        else:
            index_x1 = np.abs(x1 - x1val).argmin()
        if x2val < x1.min() or x2val > x1.max():
            return False
        else:
            index_x2 = np.abs(x1 - x2val).argmin()

        # Get data from x_data and y_data using the indexes for x1 and x2, respectively
        x1val = x1[index_x1]
        x2val = x1[index_x2]
        y1val = y1[index_x1]
        y2val = y1[index_x2]

        # Calculate differences
        dx = x2val - x1val
        dy = y2val - y1val

        # Send calculated values to result (if needed). This will be sent to command line
        result = [dx, dy] # <--- HERE IS THE RESULT TO SEND TO COMMAND LINE

        # Create summary row to add to the report. The values must match the column names in REPORT_HEADERS
        row_to_report = [self.consecutive_number, name1, x1val, x2val, dx, y1val, y2val, dy]

        # Update Window Widgets
        if self.app and not self.commandline:                                                                           #|
            # Put values to the entries
            self.set_entry_value(self.x1_entry, x1val)
            self.set_entry_value(self.x2_entry, x2val)
            self.set_entry_value(self.y1_entry, y1val)
            self.set_entry_value(self.y2_entry, y2val)
            self.set_entry_value(self.dx_entry, dx)
            self.set_entry_value(self.dy_entry, dy)
        return row_to_report

if __name__ == "__main__":
    tester = TemplateClass()
    pass

