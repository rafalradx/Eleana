#!/usr/bin/python3
import numpy as np
from scipy.integrate import cumulative_trapezoid, trapezoid
from assets.SubprogMethods import SubMethods
from assets.Error import Error

# Change the line below to match your folder in subprogs and UI file
from integrate_region.IntegrateRegionui import IntegrateRegionUI as WindowGUI
#from IntegrateRegionui import IntegrateRegionUI as WindowGUI

TITLE = 'Integrate region'              # <--- TITLE OF THE WINDOW
WORK_ON_START = False                   # <--- IF TRUE THEN CALCULATION ON CURRENT SELECTED DATA IS PERFORMED ON WINDOW OPENING
ON_TOP = True                           # <--- IF TRUE THE WINDOW WILL BE ALWAYS ON TOP
REGIONS = True                          # <--- IF TRUE THE DATA WILL BE EXTRACTED FROM REGIONS IN SELF.ELEANA.COLOR_SPAN
TWO_SETS = False                        # <--- IF TRUE THEN FIRST AND SECOND DATA WILL BE AVAILABLE FOR CALCULATIONS
REPORT = True                           # <--- IF TRUE THEN REPORT WILL BE CREATED AFTER CALCULATIONS
STACK_SEP = True                        # <--- IF TRUE THEN EACH DATA IS A STACK WILL BE CALCULATED SEPARATELY
                                        #      WHEN FALSE THEN YOU MUST CREATE A METHOD THAT CALCS OF THE WHOLE STACK
                                        # ||| CREATE NAME OF COLUMS FOR REPORT TO BE CREATED
REPORT_HEADERS = ['Nr', 'Name', 'Parameter values \n for consecutive data in stack', 'Integral Value'] # <--- Define names of columns in the Report
DATA_LABEL_WIDGET = 'data_label'        # <--- ID OF THE LABEL WIDGET WHERE NAME OF CURRENTLY SELECTED DATA WILL APPEAR.
                                        #      THE LABEL MUST EXIST IN THE GUI. IF NOT USED SET THIS TO NONE


class IntegrateRegion(SubMethods, WindowGUI):
    ''' THIS IS STANDARD PART THAT SHOULD BE COPIED WITHOUT MODIFICATIONS '''
    def __init__(self, app=None, which='first', batch_mode=False):
        if app and not batch_mode:
            # Initialize window if app is defined and not batch mode is set
            WindowGUI.__init__(self, app.mainwindow)
        self.get_from_region = REGIONS
        self.create_report = REPORT
        self.collected_reports = {'headers':REPORT_HEADERS, 'rows':[]}
        # Use second data
        self.use_second = TWO_SETS
        SubMethods.__init__(self, app=app, which=which, use_second=self.use_second, stack_sep = STACK_SEP, data_label = DATA_LABEL_WIDGET, work_on_start = WORK_ON_START)
    def configure_window(self):
        # Configure Window if app is defined
        self.mainwindow.title(TITLE)
        self.mainwindow.attributes('-topmost', ON_TOP)

        # References
        # HERE DEFINE YOUR REFERENCES TO WIDGETS
        # AND CONFIGURE CUSTOM WIDGETS
        self.check_double_integration = self.builder.get_object('check_double', self.mainwindow)
        self.field_value = self.builder.get_object('field_value', self.mainwindow)


    # STANDARD METHODS FOR BUTTON EVENTS ON CLICK
    def ok_clicked(self):
        self.consecutive_number += 1
        self.perform_single_calculations()      # <-- This is standard function in SubprogMethods

    def process_group_clicked(self):
        self.perform_group_calculations()        # <-- This is standard function in SubprogMethods
    def show_report_clicked(self):
        self.show_report()                       # <-- This is standard function in SubprogMethods
    def set_double_integration(self):
        self.perform_single_calculations()       # <-- This is standard function in SubprogMethods

    def clear_report_clicked(self):
        self.clear_report()                      # <-- This is standard function in SubprogMethods

    def perform_command_line_calc(self):
        print('Command line calculation')
        pass

    def calculate(self, original_data = None,
                        name = None,
                        stk_index = None,
                        y_data = None,
                        x_data = None,
                        z_data = None,
                        double=None):

        ''' MODIFY THIS ACCORDING TO WHAT YOU WANT TO CALCULATE
            Method that calculates something in your subprogram
            This must be prepared for a single data
            But you must check if it works for
            all possible data types.
            normalize_to, y_data and/or x_data are required
            only for testing the function
        '''
        # When self.original_data contain data class then ignore x_data, y_data
        # and other parameters sent to this function

        if self.original_data and self.app is None:
            x_data = self.original_data.x
            y_data = self.original_data.y
            z_data = self.original_data.z
            name = self.original_data.name_nr
        #if not x_data or not y_data:
        #    Error.show(title = 'Empty set', info='It looks like there is no y data or x data to perform calculations')

        x_cal = x_data
        y_cal = y_data
        z_cal = z_data
        name_cal = name

        ''' HERE STARTS YOUR CODE 
        --------------------------
        Use:
            x_data:  contains data for x axis
            y_data:  contains data for y axis (can be complex)
            z_data:  contains data for z axis if there is a stack
        After calculation put calculated data:
            y_cal:  the results of calculations on y_data
            x_cal:  the result of calculations on x_data
            z_cal:  the result of calculations on z_data
        '''

        if not double:
            double_integration = self.check_double_integration.get()
        y_cal = cumulative_trapezoid(y_data, x_data, initial=0)
        integral = trapezoid(y_data,x_data)
        if double_integration:
            y_cal2 = cumulative_trapezoid(y_cal, x_data, initial=0)
            integral = trapezoid(y_cal, x_data)
            y_cal = y_cal2

        # Update values in GUI widgets
        self.field_value.delete(0, 'end')
        self.field_value.insert(0, str(integral))

        # Construct line for the report
        to_result_row = [self.consecutive_number, name_cal, z_cal, integral]
        # Upadte results of the calculations
        self.update_result_data(y = y_cal, x = x_cal)
        return to_result_row
'''

------------------------------------------------------------------------------
----         Trzeba poprawić procedury obliczeń dla Stack                 ----
----         Przy stack 2D pojawia się błąd w Grapherze. Prawdopodobnie
            brakuje danych w widmie obliczonym ze stack.
            Dla pojedynczego wydaje się działać ok

'''
















if __name__ == "__main__":
    TEST_SUBPROG = True
    ir = IntegrateRegion()
    ir.collected_reports = {'headers':  ['nazwa', 'zakres','wartość1', 'wartość2'],
                            'rows':[['widmo 2',2,3,4],
                                    ['widmo 3',2,6,5],
                                    ['widmo 4',10,43,54]
                                    ]
                            }
    ir.show_report()
    pass

