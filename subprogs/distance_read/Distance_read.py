#!/usr/bin/python3
# IMPORT MODULES NEEDED
# -- Here is an example --
import numpy as np

# General setting of the application. Here is an example
# File/Path/Class settings
SUBPROG_FOLDER = 'distance_read'     # <--- SUBFOLDER IN SUBPROGS CONTAINING THIS FILE
GUI_FILE = 'DistanceReadui.py'       # <--- PYTHON FILE GENERATED BY PYGUBU-DESIGNER CONTAINING GUI
GUI_CLASS = 'DistanceReadUI'         # <--- CLASS NAME IN GUI_FILE THAT BUILDS THE WINDOW

# Window settings
TITLE = 'Calculate XY Distance'              # <--- TITLE OF THE WINDOW
WORK_ON_START = False                   # <--- IF TRUE THEN CALCULATION ON CURRENT SELECTED DATA IS PERFORMED UPON OPENING OF THE SUBPROG
ON_TOP = True                           # <--- IF TRUE THE WINDOW WILL BE ALWAYS ON TOP
DATA_LABEL_WIDGET = 'data_label'        # <--- ID OF THE LABEL WIDGET WHERE NAME OF CURRENTLY SELECTED DATA WILL APPEAR.
                                        #      THE LABEL WIDGET OF THE SAME ID NAME MUST EXIST IN THE GUI. IF NOT USED SET THIS TO NONE
# Data settings
REGIONS = False                          # <--- IF TRUE THE DATA WILL BE EXTRACTED FROM REGIONS IN SELF.ELEANA.COLOR_SPAN
TWO_SETS = False                        # <--- IF TRUE THEN FIRST AND SECOND DATA WILL BE AVAILABLE FOR CALCULATIONS
STACK_SEP = True                        # <--- IF TRUE THEN EACH DATA IN A STACK WILL BE CALCULATED SEPARATELY
                                        #      WHEN FALSE THEN YOU MUST CREATE A METHOD THAT CALCS OF THE WHOLE STACK

# Report settings
REPORT = True                           # <--- IF TRUE THEN REPORT WILL BE CREATED AFTER CALCULATIONS
REPORT_HEADERS = ['Nr', 'Name', 'X1', 'X2', 'dX', 'Y1', 'Y2', 'dY'] # <--- Define names of columns in the Report
REPORT_DEFAULT_X = 0                    # <--- INDEX IN REPORT_HEADERS USED TO SET NAME OF COLUMN THAT IS USED AS DEFAULT X IN THE REPORT
REPORT_DEFAULT_Y = 7                    # <--- INDEX IN REPORT_HEADERS USED TO SET NAME OF COLUMN THAT IS USED AS DEFAULT Y IN THE REPORT
REPORT_NAME_X =  'Data Number'          # <--- NAME OF X AXIS IN THE REPORT
REPORT_NAME_Y =  'dY Value'             # <--- NAME OF Y AXIS IN THE REPORT
REPORT_UNIT_X = ''                      # <--- NAME OF X UNIT IN THE CREATED REPORT
REPORT_UNIT_Y = ''                      # <--- NAME OF Y UNIT IN THE CREATED REPORT

# Cursors on graph
CURSOR_TYPE = 'Crosshair'               # <--- USE CURSORS: 'None', 'Continuous read XY', 'Selection of points with labels'
                                        #       'Selection of points', 'Numbered selections', 'Free select', 'Crosshair', 'Range select'

# ----------------------------------------------------------------------------------------------------
#   -- Here starts obligatory part of the application                                               #|
#   -- In general it should not be modified                                                         #|
#                                                                                                   #|
cmd_to_import = GUI_FILE[:-3] + ' import ' + GUI_CLASS + ' as WindowGUI'                            #|
if __name__ == "__main__":                                                                          #|
    cmd_to_import = 'from ' + cmd_to_import                                                         #|
else:                                                                                               #|
    cmd_to_import = 'from ' + SUBPROG_FOLDER + '.' + cmd_to_import                                  #|
exec(cmd_to_import)                                                                                 #|
from assets.Error import Error                                                                      #|
from assets.SubprogMethods import SubMethods                                                        #|
class DistanceRead(SubMethods, WindowGUI):                                                          #|
    ''' THIS IS STANDARD CONSTRUCTOR THAT SHOULD NOT BE MODIFIED '''                                #|
    def __init__(self, app=None, which='first', batch_mode=False):                                  #|
        if app and not batch_mode:                                                                  #|
            # Initialize window if app is defined and not batch mode is set                         #|
            WindowGUI.__init__(self, app.mainwindow)                                                #|
        self.get_from_region = REGIONS                                                              #|
        self.create_report = REPORT                                                                 #|
        self.collected_reports = {'headers':REPORT_HEADERS,                                         #|
                                  'rows':[],                                                        #|
                                  'x_name':REPORT_NAME_X,                                           #|
                                  'y_name':REPORT_NAME_Y,                                           #|
                                  'default_x':REPORT_HEADERS[REPORT_DEFAULT_X],                     #|
                                  'default_y':REPORT_HEADERS[REPORT_DEFAULT_Y],                     #|
                                  'x_unit':REPORT_UNIT_X, 'y_unit':REPORT_UNIT_Y}                   #|
        # Use second data                                                                           #|
        self.use_second = TWO_SETS                                                                  #|
        if CURSOR_TYPE == 'None':
            cursor_mode = None
        else:
            cursor_mode = {'type':CURSOR_TYPE, 'x':[], 'y':[], 'z':[]}
        SubMethods.__init__(self, app=app,                                                          #|
                            which=which,                                                            #|
                            use_second=self.use_second,                                             #|
                            stack_sep = STACK_SEP,                                                  #|
                            data_label = DATA_LABEL_WIDGET,                                         #|
                            work_on_start = WORK_ON_START,                                          #|
                            window_title = TITLE,                                                   #|
                            on_top=ON_TOP,                                                          #|
                            cursor_mode = cursor_mode)                                              #|
                                                                                                    #|
    # STANDARD METHODS FOR BUTTON EVENTS ON CLICK                                                   #|
    def ok_clicked(self):                                                                           #|
        ''' [-OK-] button                                                                           #|
            This is standard function in SubprogMethods '''                                         #|
        self.perform_single_calculations()                                                          #|
                                                                                                    #|
    def process_group_clicked(self):                                                                #|
        ''' [-Process Group-] button                                                                #|
            This is standard function in SubprogMethods '''                                         #|
        self.perform_group_calculations()                                                           #|
                                                                                                    #|
    def show_report_clicked(self):                                                                  #|
        ''' [-Show Report-] button                                                                  #|
            This is standard function in SubprogMethods '''                                         #|
        self.show_report()                                                                          #|
                                                                                                    #|
    def clear_report_clicked(self):                                                                 #|
        ''' [-Clear Report-] button                                                                 #|
            This is standard function in SubprogMethods '''                                         #|
        self.clear_report()                                                                         #|
                                                                                                    #|
    #                                                                                               #|
    # Here ends the obligatory part of the application                                              #|
    # Your code starts from here                                                                    #|
    #-------------------------------------------------------------------------------------------------

    def configure_window(self):
        # Define additional window configuration if needed
        #self.mainwindow =

        # Define references to your additional widgets and configuration
        self.x1_entry = self.builder.get_object('x1_entry', self.mainwindow)
        self.x2_entry = self.builder.get_object('x2_entry', self.mainwindow)
        self.dx_entry = self.builder.get_object('dx_entry', self.mainwindow)
        self.y1_entry = self.builder.get_object('y1_entry', self.mainwindow)
        self.y2_entry = self.builder.get_object('y2_entry', self.mainwindow)
        self.dy_entry = self.builder.get_object('dy_entry', self.mainwindow)
        self.check_keep_track = self.builder.get_object('check_track_minmax', self.mainwindow)
        self.keep_track = False
        # Create validate methods for CTkEntries. Use this to enter only numbers in the entries
        self.validate_command = (self.mainwindow.register(self.validate_number), '%P')
        self.x1_entry.configure(validate="key", validatecommand=self.validate_command)
        self.x2_entry.configure(validate="key", validatecommand=self.validate_command)
        self.y1_entry.configure(validate="key", validatecommand=self.validate_command)
        self.y2_entry.configure(validate="key", validatecommand=self.validate_command)

        # Set disabled field
        self.dx_entry.configure(state='disabled')
        self.dy_entry.configure(state='disabled')

    def graph_action(self, variable=None, value=None):
        ''' Do something when cursor action on graph was done '''
        print('uhfu weuhfuhw fuhewfu qhuif')

    def find_minmax_clicked(self):
        print('Find min/max')

    def track_minmax_clicked(self):
        self.keep_track = self.check_keep_track.get()
        if self.keep_track:
            self.find_minmax_clicked()

    def calculate_stack(self, x, y, name, z = None, stk_index = None):
        ''' If STACK_SEP is False it means that data in stack should
            not be treated as separate data but are calculated as whole
            If not used, leave it as it is
        '''
        info__ = 'There is no method defined for Stack calculations'
        if self.app is not None:
            Error.show(info=info__)
        else:
            print(info__)

    # Here starts your main algorithm that performs a calculations
    # On a single data
    def calculate(self, dataset = None, name = None, stk_index = None, y = None, x = None, z = None,
                  double=None # <--- Add your additional variables
                  ):
        # Do not remove the line below
        x_data, y_data, z_data, name, x_cal, y_cal, z_cal, name_cal = self.prep_calc_data(dataset, x, y, z, name)

        ''' 
        Your code starts here 
        ---------------------
        Use:
            x_data:  contains original data for x axis
            y_data:  contains original data for y axis (can be complex)
            z_data:  contains original data for z axis if there is a stack
        After calculation put calculated data to:
            y_cal:  the results of calculations on y_data
            x_cal:  the result of calculations on x_data
            z_cal:  the result of calculations on z_data
            result: the value of resulted calculations 
        '''

        # Send calculated values to result (if needed)
        result = None # <--- HERE
        # Create summary row to add to the report
        to_result_row = [self.consecutive_number, name_cal, z_cal, result]  # Here

        # ------- AFTER CALCULATIONS ---------
        # You must adjust this according to your needs. Below are examples
        # Update Window Widgets
        if not self.batch:
            self.field_value.delete(0, 'end')
            self.field_value.insert(0, str(result)) # <--- Put 'result' to the widget


        #---------------------------------------------------------------------------------------------
        # Construct line for the report if needed                                                   #|
        # This is obligatory part of the function                                                   #|
        if not self.batch:                                                                          #|
            # Update results of the calculations                                                    #|
            self.update_result_data(y=y_cal, x=x_cal, z=z_cal)                                      #|
            return to_result_row # <--- Return this if report is going to be                        #|
        else:                                                                                       #|
            return result # <-- Return this to commmand line                                        #|
        #---------------------------------------------------------------------------------------------

# THIS IS FOR TESTING COMMAND LINE
if __name__ == "__main__":
    ir = IntegrateRegion()
    x_data = np.array([1,2,3,4,5,6])
    y_data = np.array([4,3,5,3,5,6])
    double = False
    integral = ir.calculate(x=x_data, y=y_data, double = double)
    print(integral)

