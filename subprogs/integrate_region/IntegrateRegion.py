#!/usr/bin/python3
import numpy as np
from scipy.integrate import cumulative_trapezoid, trapezoid
from assets.SubprogMethods import SubMethods
from assets.Error import Error

# Change the line below to match your folder in subprogs and UI file
from integrate_region.IntegrateRegionui import IntegrateRegionUI as WindowGUI

TITLE = 'Integrate region'  # <--- TITLE OF THE WINDOW
ON_TOP = True               # <--- IF TRUE THE WINDOW WILL BE ALWAYS ON TOP
REGIONS = True              # <--- IF TRUE THE DATA WILL BE EXTRACTED FROM REGIONS IN SELF.ELEANA.COLOR_SPAN
TWO_SETS = False            # <--- IF TRUE THEN FIRST AND SECOND DATA WILL BE AVAILABLE
REPORT = True               # <--- IF TRUE THEN RAPORT WILL BE CREATED AFTER CALCULATIONS

class IntegrateRegion(SubMethods, WindowGUI):
    ''' THIS IS STANDARD PART THAT SHOULD BE COPIED WITHOUT MODIFICATIONS '''
    def __init__(self, app=None, which='first', batch_mode=False):
        if app and not batch_mode:
            # Initialize window if app is defined and not batch mode is set
            WindowGUI.__init__(self, app.mainwindow)
        self.get_from_region = REGIONS
        self.create_report = REPORT
        # Use second data
        self.use_second = TWO_SETS
        SubMethods.__init__(self, app=app, which=which, use_second=self.use_second)
    def configure_window(self):
        # Configure Window if app is defined
        self.mainwindow.title(TITLE)
        self.mainwindow.attributes('-topmost', ON_TOP)

        # References
        # HERE DEFINE YOUR REFERENCES TO WIDGETS
        # AND CONFIGURE CUSTOM WIDGETS
        self.check_double_integration = self.builder.get_object('check_double', self.mainwindow)
        self.field_value = self.builder.get_object('field_value', self.mainwindow)

    def set_double_integration(self):
        double_integration = self.check_double_integration.get()
        if self.eleana.devel_mode:
            print('Double integration set: ', str(double_integration))
        self.perform_calculation(double = double_integration)

    def perform_calculation(self, double = False, original_data= None, y_data=None, x_data=None):
        ''' MODIFY THIS ACCORDING TO WHAT YOU WANT TO CALCULATE
            Method that calculates something in your subprogram
            This must be prepared for a single data
            But you must check if it works for
            all possible data types.
            normalize_to, y_data and/or x_data are required
            only for testing the function
        '''

        if not double:
            double_integration = self.check_double_integration.get()
        if not self.original_data:
            return
        else:
            x_data = self.original_data.x
            y_data = self.original_data.y

        # Process data in Y
        if y_data is not None:
            if y_data.shape[0] == 0:
                # If np.array is empty - return
                if self.eleana.devel_mode:
                    print('Integrate region -> perform_calculation(): Empty Y')
                return

            if len(y_data.shape) == 1:
                y_cal = cumulative_trapezoid(y_data, x_data, initial=0)
                integral = trapezoid(y_data,x_data)
                if self.check_double_integration.get():
                    y_data = cumulative_trapezoid(y_cal, x_data, initial=0)
                    integral = trapezoid(y_cal, x_data)
                    y_cal = y_data

        #     elif len(y_data.shape) == 2:
        #         single_report = {'name_nr':'',
        #                          'name_stk':'',
        #                          'double':False,
        #                          'integral':0}
        #         report = []
        #         i = 0
        #         name_nr = self.original_data.name_nr
        #         list_of_processed_y = []
        #         for each_y in y_data:
        #             name_stk = self.original_data.stk_names[i]
        #             double = double_integration
        #             y_cal = cumulative_trapezoid(y_data, x_data, initial=0)
        #             integral = trapezoid(y_data, x_data)
        #             if self.check_double_integration.get():
        #                 y_data = cumulative_trapezoid(y_cal, x_data, initial=0)
        #                 integral = trapezoid(y_cal, x_data)
        #                 y_cal = y_data
        #             list_of_processed_y.append(y_cal)
        #             y_cal = np.array(list_of_processed_y)
        #
        self.field_value.delete(0, 'end')
        self.field_value.insert(0, str(integral))
        # Leve the following line here
        self.update_result_data(x = x_data, y = y_cal)

if __name__ == "__main__":
    pass

