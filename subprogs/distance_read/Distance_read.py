#!/usr/bin/python3
# IMPORT MODULES NEEDED
# -- Here is an example --
import numpy as np

from subprogs.integrate_region.IntegrateRegion import RESULT_CREATE

# General setting of the application. Here is an example
# File/Path/Class settings

SUBPROG_FOLDER = 'distance_read'        # <--- SUBFOLDER IN SUBPROGS CONTAINING THIS FILE
GUI_FILE = 'DistanceReadui.py'          # <--- PYTHON FILE GENERATED BY PYGUBU-DESIGNER CONTAINING GUI
GUI_CLASS = 'DistanceReadUI'            # <--- CLASS NAME IN GUI_FILE THAT BUILDS THE WINDOW

# Window settings
TITLE = 'Calculate XY Distance'         # <--- TITLE OF THE WINDOW
ON_TOP = True                           # <--- IF TRUE THE WINDOW WILL BE ALWAYS ON TOP
DATA_LABEL = 'data_label'               # <--- ID OF THE LABEL WIDGET WHERE NAME OF CURRENTLY SELECTED DATA WILL APPEAR.
                                        #      THE LABEL WIDGET OF THE SAME ID NAME MUST EXIST IN THE GUI. IF NOT USED SET THIS TO NONE
NAME_SUFFIX = ''                        # <--- DEFINES THE SUFFIX THAT WILL BE ADDED TO NAME OF PROCESSED DATA
AUTO_CALCULATE = False                  # <--- DEFINES IF CALCULATION IS AUTOMATICALLY PERFORMED UPON DATA CHANGE IN GUI

# Data settings
REGIONS_FROM = 'scale'                  # <--- DEFINES IF DATA WILL BE EXTRACTED:
#REGIONS_FROM = 'selection'             # 'none' - DO NOT EXTRACT
                                        # 'scale' - EXTRACT DATA BETWEEN X MIN X MAX
                                        # 'sel' - EXTRACT DATA FROM SELECTED RANGE

USE_SECOND = False                      # <--- IF TRUE THEN FIRST AND SECOND DATA WILL BE AVAILABLE FOR CALCULATIONS
STACK_SEP = True                        # <--- IF TRUE THEN EACH DATA IN A STACK WILL BE CALCULATED SEPARATELY
                                        #      WHEN FALSE THEN YOU MUST CREATE A METHOD THAT CALCS OF THE WHOLE STACK
RESULT_CREATE = ''
#RESULT_CREATE = 'add'                  # <--- DETEMINES IF PROCESSED DATA SHOULD BE ADDED TO RESULT_DATASET
#RESULT_CREATE = 'replace'              #      'ADD' OR 'REPLACE' IS SELF EXPLANATORY
                                        #      ANY OTHER VALUES MEANS NOT RESULT CREATION

# Report settings
REPORT_CREATE = True                    # <--- IF TRUE THEN REPORT WILL BE CREATED AFTER CALCULATIONS
REPORT_SKIP_FOR_STK = False
REPORT_WINDOW_TITLE = 'Results of distance measurements'
REPORT_HEADERS = ['Nr',
                  'Name',
                  'X1',
                  'X2',
                  'dX',
                  'Y1',
                  'Y2',
                  'dY']                  # <--- Define names of columns in the Report
REPORT_DEFAULT_X = 0                    # <--- INDEX IN REPORT_HEADERS USED TO SET NAME OF COLUMN THAT IS USED AS DEFAULT X IN THE REPORT
REPORT_DEFAULT_Y = 7                    # <--- INDEX IN REPORT_HEADERS USED TO SET NAME OF COLUMN THAT IS USED AS DEFAULT Y IN THE REPORT
REPORT_NAME = "Distance measurements"
REPORT_NAME_X =  'Data Number'          # <--- NAME OF X AXIS IN THE REPORT
REPORT_NAME_Y =  'dY Value'             # <--- NAME OF Y AXIS IN THE REPORT
REPORT_UNIT_X = ''                      # <--- NAME OF X UNIT IN THE CREATED REPORT
REPORT_UNIT_Y = ''                      # <--- NAME OF Y UNIT IN THE CREATED REPORT
REPORT_TO_GROUP = 'RESULT Distance'     # <--- DEFAULT GROUP NAME TO WHICH REPORT WILL BE ADDED

# Cursors on graph
CURSOR_CHANGING = False                  # <--- IF TRUE THEN CURSOR SELECTION IN MAIN GUI WILL BE DISABLED
CURSOR_TYPE = 'Free select'               # <--- USE CURSORS: 'None', 'Continuous read XY', 'Selection of points with labels'
                                        #       'Selection of points', 'Numbered selections', 'Free select', 'Crosshair', 'Range select'
CURSOR_LIMIT = 2                        # <--- SET THE MAXIMUM NUMBER OF CURSORS THAT CAN BE SELECTED. FOR NO LIMIT SET 0
CURSOR_CLEAR_ON_START = True
CURSOR_REQUIRED = 2                     # <--- MINIMUM NUMBER OF CURSORS TO PROCESS THE CALCULATIONS
                                        #      SET TO 0 FOR NO CHECKING
CURSOR_REQ_TEXT = \
    'Please select two points.'         # <--- TEXT TO DISPLAY IF NR OF CURSORS IS LESS THAN REQUIRED
                                        #    LEAVE EMPTY IF YOU DO NOT WANT TO SHOW THE ERROR
CURSOR_OUTSIDE_X = False                # <--- CHECK IF ALL CURSORS ARE BETWEEN Xmin Xmax FOR SELF>DATA_FOR_CALCULATIONS
CURSOR_OUTSIDE_Y = False
CURSOR_OUTSIDE_TEXT = \
                'One or more selected points are outside the (x, y) range of data.'
'''
##################################
#    END OF SUBPROG SETTINGS     #
#  DO NOT MODIFY LINES BELOW     #
##################################'''

cmd_to_import = GUI_FILE[:-3] + ' import ' + GUI_CLASS + ' as WindowGUI'                            #|
if __name__ == "__main__":                                                                          #|
    cmd_to_import = 'from ' + cmd_to_import                                                         #|
else:                                                                                               #|
    cmd_to_import = 'from ' + SUBPROG_FOLDER + '.' + cmd_to_import                                  #|
exec(cmd_to_import)                                                                                 #|
from assets.Error import Error                                                                      #|
from assets.SubprogMethods2 import SubMethods_02 as Methods                                                    #|
class DistanceRead(Methods, WindowGUI):                                                       #|
    def __init__(self, app=None, which='first', commandline=False):  # |
        if app and not commandline:
            # Initialize window if app is defined and not commandline                               #|
            WindowGUI.__init__(self, app.mainwindow)
        # Create settings for the subprog                                                           #|
        self.subprog_settings = {'title': TITLE, 'on_top': ON_TOP, 'data_label': DATA_LABEL,
                                 'name_suffix': NAME_SUFFIX, 'auto_calculate': AUTO_CALCULATE,
                                 'result': RESULT_CREATE}
        self.regions = {'from': REGIONS_FROM}
        self.report = self.report = {'nr': 1,
                                     'create': REPORT_CREATE,
                                     'headers': REPORT_HEADERS,
                                     'rows': [],
                                     'x_name': REPORT_NAME_X,
                                     'y_name': REPORT_NAME_Y,
                                     'default_x': REPORT_HEADERS[REPORT_DEFAULT_X],
                                     'default_y': REPORT_HEADERS[REPORT_DEFAULT_Y],
                                     'x_unit': REPORT_UNIT_X,
                                     'y_unit': REPORT_UNIT_Y,
                                     'to_group': REPORT_TO_GROUP,
                                     'report_skip_for_stk': REPORT_SKIP_FOR_STK,
                                     'report_window_title': REPORT_WINDOW_TITLE,
                                     'report_name': REPORT_NAME
                                     }
        self.subprog_cursor = {'type': CURSOR_TYPE, 'changing': CURSOR_CHANGING, 'limit': CURSOR_LIMIT,
                               'clear_on_start': CURSOR_CLEAR_ON_START, 'cursor_required': CURSOR_REQUIRED, 'cursor_req_text':CURSOR_REQ_TEXT,
                               'cursor_outside_x':CURSOR_OUTSIDE_X, 'cursor_outside_y':CURSOR_OUTSIDE_Y,
                               'cursor_outside_text':CURSOR_OUTSIDE_TEXT}
        # Use second data
        self.use_second = USE_SECOND
        # Treat each data in stack separately
        self.stack_sep = STACK_SEP  # |
        Methods.__init__(self, app=app, which=which, commandline=commandline)


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
    pass

