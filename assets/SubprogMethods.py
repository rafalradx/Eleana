from assets.Observer import Observer
import copy
import numpy as np

class SubMethods():
    def __init__(self, app=None, which='first'):
        # Set get_from_region to use selected range for data
        self.get_from_region = True
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
        # Do not build window if app is not defined
        if self.app:
            # Create window
            self.configure_window()
            # Create observer
            self.observer = Observer(self.eleana, self)
            self.eleana.notify_on = True
            # Initialize data to modify
            self.get_data(start=True)
            # Set current position in Results Dataset
            self.result_index = len(self.eleana.results_dataset)

    def get(self):
        ''' Returns self.response to the main application after close '''
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event=None):
        ''' Close the window without changes '''
        self.response = None
        # Unregister observer
        self.eleana.detach(self.observer)
        self.mainwindow.destroy()

    def get_data(self, start=False):
        ''' Makes a copy of the selected data and stores it in self.original_data.
            You may perform calculations on self.original_data. '''
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
            self.original_data = None
            self.result_data = None
            return False
        # Create reference to original data
        self.original_data = copy.deepcopy(self.eleana.dataset[index])
        # Create reference to data in results
        self.result_index = self.eleana.selections['result']
        self.result_data = self.eleana.results_dataset[self.result_index]
        if self.get_from_region:
            self.extract_region()
        if start:
            self.perform_calculation()

    def data_changed(self):
        ''' Activate get_data when selection changed.
            This is triggered by the Observer.   '''
        self.get_data()
        self.perform_calculation()

    def update_result_data(self, y=None, x=None):
        ''' Move calculated data in y and x to self.eleana.result_dataset. '''
        if y is not None:
            if self.app:
                self.result_data.y = y
            else:
                print('Result Y:')
                print(y)
        if x is not None:
            if self.app:
                self.result_data.x = x
            else:
                print('Result X:')
                print(x)
        if self.app:
            self.grapher.plot_graph()

    def ok_clicked(self, value=None):
        ''' Triggers 'perform_calculation' when Calc/Ok button is clicked.
            The button must have command = ok_clicked
        '''
        self.perform_calculation()

    def process_group(self):
        ''' Triggers 'perform_calculation' for all data in the current group. '''
        self.app.clear_results(skip_question=True)
        self.mainwindow.config(cursor='watch')
        spectra = copy.copy(self.app.sel_first._values)
        current_first_sel = self.eleana.selections['first']
        del spectra[0]
        i = 0
        for spectrum in spectra:
            self.app.first_to_result(name=spectrum)
            index = self.eleana.get_index_by_name(spectrum)
            self.original_data = copy.deepcopy(self.eleana.dataset[index])
            self.result_data = self.eleana.results_dataset[i]
            self.perform_calculation()
            i += 1
        self.mainwindow.config(cursor='')

    def extract_region(self):
        ''' Extract data on the basis of selected ranges in self.eleana.color_span['ranges'] '''
        ranges = self.eleana.color_span['ranges']
        if not ranges:
            return
        x = self.original_data.x
        y = self.original_data.y
        is_2D = len(y.shape) == 2
        indexes = []
        for range_ in ranges:
            idx = np.where((x >= range_[0]) & (x <= range_[1]))[0]
            indexes.extend(idx.tolist())
        extracted_x = x[indexes]
        if is_2D:
            extracted_y = y[:, indexes]
        else:
            extracted_y = y[indexes]
        self.original_data.x = extracted_x
        self.original_data.y = extracted_y
