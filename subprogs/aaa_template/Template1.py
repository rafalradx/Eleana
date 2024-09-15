# -----------------------------------------------------------------------------------------------------------
# !/usr/bin/python3                                                                             #           |
import numpy as np                                                                              #           |
from assets.SubprogMethods import SubMethods                                                    #           |
# ----------------------------------------------------------------------------------------------------------|



#    <------------ change this ----------------->        <--this-->    <--KEEP-->
from 'FOLDER_IN_SUBPROG.FILE_CONTAINING_UI_CLASS' import 'UI_CLASS' as SubprogGUI

WINDOW_TITLE =  'Window Title'    # Define your window title
ON_TOP = True                     # Set always on top?




# -----------------------------------------------------------------------------------------------------------
class IntegrateRegion(SubMethods, GUI):                                                         #           |
    def __init__(self, app=None, which='first', batch_mode=False):                              #           |
        self.get_from_region = 'False'                                                          #           |
        if app and not batch_mode:                                                              #           |
            # Initialize window if app is defined and not batch mode is set                     #           |
            SubprogGUI.__init__(self, app.mainwindow)                                           #           |
        SubMethods.__init__(self, app=app, which=which, batch_mode=batch_mode)                  #           |
        self.custom_init()                                                                      #           |
    def configure_window(self):                                                                 #           |
        # Configure Window if app is defined                                                    #           |
        self.mainwindow.title(ON_TOP)                                                           #           |
        self.mainwindow.attributes('-topmost', ON_TOP)                                          #           |
# -----------------------------------------------------------------------------------------------------------

    def custom_init(self):
        ''' Add your custom the methods to __init__()'''
        # If selection is needed set this True
        #                    <-change->
        self.get_from_region = 'False'

        # References if needed. (Here is an example)
        # self.check_double_integration = self.builder.get_object('check_double', self.mainwindow)


    def perform_calculation(self, normalize_to=None, y_data=None, x_data=None):
        ''' MODIFY THIS ACCORDING TO WHAT YOU WANT TO CALCULATE
            Method that calculates something in your subprogram
            This must be prepared for a single data
            But you must check if it works for
            all possible data types.
            normalize_to, y_data and/or x_data are required
            only for testing the function
        '''
        if not self.original_data:
            return
        else:
            x = self.original_data.x
            y = self.original_data.y

        # THE CODE HERE
        # x_cal should finally contain calculated x
        # y_cal should finally contain calculated y

        # Leve the following line here
        self.update_result_data(x=x_cal, y=y_calc)





if __name__ == "__main__":
    pass

