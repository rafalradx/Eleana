#!/usr/bin/python3

''' For testing the subprog set this True
    For use in Main App set this False
'''
TEST = False
# ---------------
if not TEST:
    from normalize.Normalizeui import NormalizeUI
    from CTkSpinbox import CTkSpinbox
    from Observer import Observer
else:
    from Normalizeui import NormalizeUI

# Import What you need
import copy
import numpy as np

# Your Class
class Normalize(NormalizeUI):
    ''' THIS IS STANDARD PART THAT SHOULD BE COPIED WITHOUT MODIFICATIONS '''
    def __init__(self, app  = None, which = 'first', batch_mode = False):
        if app:
            self.app = app
            self.master = self.app.mainwindow
            self.eleana = self.app.eleana
            self.grapher = self.app.grapher
        else:
            self.app = None
            self.master = None
            self.eleana = None
            self.grapher = None
        # Set to which selection 'First' or 'Second'
        self.which = which
        # Create batch mode state
        self.batch = batch_mode
        # Do not build window if batch mode is true or app is not defined
        if self.batch == False and self.app:
            # Create window
            if self.app:
                super().__init__(self.master)
                # Configure the window
                self.configure_window()
            # Create observer
            self.observer = Observer(self.eleana, self)
            self.eleana.notify_on = True
            # Initialize data to modify
            self.get_data(start=True)
            # Set current position in Results Dataset
            self.result_index = len(self.eleana.results_dataset)
    ''' END OF STANDARD PART '''

    def configure_window(self):
        # Configure Window
        self.mainwindow.title('Normalize amplitude')   # Title of the Window Bar
        self.mainwindow.attributes('-topmost', True)   # True - always on top

        # The custom modification of the window
        # HERE: Replace tk Spinbox with CTkSpinbox
        self.spinboxFrame = self.builder.get_object('spinboxFrame', self.mainwindow)
        self.spinbox = self.builder.get_object('spinbox', self.mainwindow)
        self.spinbox.grid_remove()
        self.spinbox = CTkSpinbox(master=self.spinboxFrame, wait_for=0.05, command=self.ok_clicked, min_value=0,
                                  step_value=0.02, scroll_value=0.01, start_value=1)
        self.spinbox.grid(column=0, row=0, sticky='ew')

    def perform_calculation(self, normalize_to = None, y_data = None, x_data = None):
        ''' MODIFY THIS ACCORDING TO WHAT YOU WANT TO CALCULATE
            Method that calculates something in your subprogram
            This must be prepared for a single data
            But you must check if it works for
            all possible data types.
            normalize_to, y_data and/or x_data are required
            only for testing the function
        '''

        if not normalize_to:
            normalize_to = float(self.spinbox.get())
            y_data = self.original_data.y
            x_data = self.original_data.x

        # Process data in Y
        if y_data is not None:
            if y_data.shape[0] == 0:
                # If np.array is empty - return
                return
            if len(y_data.shape) == 2:
                ''' FOR STACK 2D '''
                # Find global maximum amplitude
                amplitudes = []
                for data in y_data:
                    amplitude = self.calc_amplitude(data)
                    amplitudes.append(amplitude)
                amplitude = sorted(amplitudes, reverse=True)[0]

                # Normalize all spectra in y_data
                list_of_processed_y = []
                for data in y_data:
                    single_y = data / amplitude * normalize_to
                    single_y = np.array(single_y)
                    list_of_processed_y.append(single_y)
                    processed_y = np.array(list_of_processed_y)
            elif len(y_data.shape) == 1:
                ''' FOR SINGLE DATA'''
                amplitude = self.calc_amplitude(y_data)
                single_y = y_data / amplitude * normalize_to
                processed_y = np.array(single_y)
        self.update_result_data(y = processed_y)

    def calc_amplitude(self, y):
        ''' This is function that performs calculation
            on a single Y data (also for stack)
            You must define your calculations here
        '''
        if np.iscomplexobj(y):
            y = np.abs(y)
        min_ = np.min(y)
        max_ = np.max(y)
        amplitude = float(max_ - min_)
        return amplitude







    # -----------------------------------------------------
    # -----------------------------------------------------
    def get(self):
        ''' Returns self.response to the main application after close '''
        ''' COPY THIS FUNCTION AS IT IS '''
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response
    def cancel(self, event=None):
        ''' Close the window without changes '''
        ''' COPY THIS FUNCTION AS IT IS '''
        self.response = None
        # Unregister observer
        self.eleana.detach(self.observer)
        self.mainwindow.destroy()
    def get_data(self, start = False):
        ''' Makes a copy of the selected data
            and stores it in self.original_data.
            You may perform calculations on self.original_data
        '''
        ''' COPY THIS FUNCTION AS IT IS '''
        # Get data from selections First or Second
        if self.eleana.selections[self.which] >= 0:
            index = self.eleana.selections[self.which]
            # Copy data from first to results using the method in app
            if start:
                self.eleana.notify_on = False
            else:
                self.eleana.notify_on = True
            if self.which == 'second':
                self.app.second_to_result()
            else:
                self.app.first_to_result()
            self.eleana.notify_on = False
        else:
            return False
        # Create reference to original data
        self.original_data = copy.deepcopy(self.eleana.dataset[index])
        # Create reference to data in results
        self.result_index = self.eleana.selections['result']
        self.result_data = self.eleana.results_dataset[self.result_index]
        if start:
            self.perform_calculation()
    def data_changed(self, variable=None, value=None):
        ''' Activate getting new data when selection changed'''
        ''' COPY THIS FUNCTION AS IT IS '''
        # This is trigerred by the observer
        self.get_data()
        self.perform_calculation()
    def update_result_data(self, y=None, x=None):
        ''' Put the modified data from y and x
            into result_dataset and replot
        '''
        ''' COPY THIS FUNCTION AS IT IS '''
        if y is not None:
            if not TEST:
                self.result_data.y = y
            else:
                print('Result Y:')
                print(y)
        if x is not None:
            if not TEST:
                self.result_data.x = x
            else:
                print('Result X:')
                print(x)
        if not TEST:
            self.grapher.plot_graph()

    def ok_clicked(self, value = None):
        ''' Triggers 'perform_calculation' for the
            current data selected in first or second
            Name of this function must match the command in the button "OK"
        '''
        ''' COPY THIS FUNCTION AS IT IS '''
        self.perform_calculation()
    def process_group(self):
        ''' Triggers 'perform_calculation' for all
            data in the current group.
            This should work without modifications
        '''
        ''' COPY THIS FUNCTION AS IT IS '''
        self.app.clear_results(skip_question=True)
        self.mainwindow.config(cursor='watch')
        spectra = copy.copy(self.app.sel_first._values)
        current_first_sel = self.eleana.selections['first']
        del spectra[0]
        i = 0
        for spectrum in spectra:
            self.app.first_to_result(name = spectrum)
            index = self.eleana.get_index_by_name(spectrum)
            self.original_data = copy.deepcopy(self.eleana.dataset[index])
            self.result_data = self.eleana.results_dataset[i]
            self.perform_calculation()
            i+=1
        self.mainwindow.config(cursor='')
    # -----------------------------------------------------
    # -----------------------------------------------------








if __name__ == "__main__":
    ''' DEFINE HERE YOUR TESTING '''
    subprogram = Normalize()

    y_data = np.array([
                        [-5+1j, 3+1j, 5+1j, 3+1j, 6+2j, 5+1j],
                        [-4+1j, 3+1j, -4+1j, 3+1, 7+1j, 2+1j]
                    ])
    subprogram.perform_calculation(normalize_to = 1, y_data = y_data)

