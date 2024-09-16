# -----------------------------------------------------------------------------------------------------------
# !/usr/bin/python3                                                                             #           |
import numpy as np                                                                              #           |
from assets.SubprogMethods import SubMethods                                                    #           |
# ----------------------------------------------------------------------------------------------------------|


#    <------------ change this ----------------->        <--this-->    <--KEEP-->
from 'FOLDER_IN_SUBPROG.FILE_CONTAINING_UI_CLASS' import 'UI_CLASS' as SubprogGUI


TITLE = 'Integrate region'  # <--- TITLE OF THE WINDOW
ON_TOP = True               # <--- IF TRUE THE WINDOW WILL BE ALWAYS ON TOP
REGIONS = True              # <--- IF TRUE THE DATA WILL BE EXTRACTED FROM REGIONS IN SELF.ELEANA.COLOR_SPAN
TWO_SETS = True             # <--- IF TRUE THEN FIRST AND SECOND DATA WILL BE AVAILABLE


# -----------------------------------------------------------------------------------------------------------
class IntegrateRegion(SubMethods, SubprogGUI):                                                         #           |
    def __init__(self, app=None, which='first', batch_mode=False):                              #           |
        self.get_from_region = 'False'                                                          #           |
        if app and not batch_mode:                                                              #           |
            # Initialize window if app is defined and not batch mode is set                     #           |
            SubprogGUI.__init__(self, app.mainwindow)                                           #           |
        SubMethods.__init__(self, app=app, which=which, batch_mode=batch_mode)                  #           |
        self.get_from_region = REGIONS                                                          #           |
        self.use_second = TWO_SETS                                                              #           |
        self.custom_init()                                                                      #           |
    def configure_window(self):                                                                 #           |
        # Configure Window if app is defined                                                    #           |
        self.mainwindow.title(ON_TOP)                                                           #           |
        self.mainwindow.attributes('-topmost', ON_TOP)                                          #           |
# -----------------------------------------------------------------------------------------------------------


    def custom_init(self):
        ''' Add your custom the methods to __init__()'''

        # References if needed. (Here is an example)
        # self.check_double_integration = self.builder.get_object('check_double', self.mainwindow)
        return

    def perform_calculation(self, normalize_to=None, y_data=None, x_data=None):
        ''' MODIFY THIS ACCORDING TO WHAT YOU WANT TO CALCULATE
            Method that calculates something in your subprogram
            This must be prepared for a single data
            But you must check if it works for
            all possible data types.
            normalize_to, y_data and/or x_data are required
            only for testing the function
        '''
        # ---------------------------------------------------------------------------------------------------
        if not self.original_data:                                                              #           |
            return                                                                              #           |
        else:                                                                                   #           |
            x_data = self.original_data.x                                                       #           |
            y_data = self.original_data.y                                                       #           |
        if self.use_second:                                                                     #           |
            x_data2 = self.original_data2.x                                                     #           |
            y_data2 = self.original_data2.y                                                     #           |
        # ---------------------------------------------------------------------------------------------------


        print(self.original_data.name_nr)
        print(self.original_data2.name_nr)

        # THE CODE HERE
        # x_cal should finally contain calculated x
        # y_cal should finally contain calculated y






        # Leve the following line here
        self.update_result_data(x=x_cal, y=y_calc)





if __name__ == "__main__":
    pass

