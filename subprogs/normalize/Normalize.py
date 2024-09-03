#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
import copy
import numpy as np
from normalize.Normalizeui import NormalizeUI
from CTkSpinbox import CTkSpinbox
from Observer import Observer

class Normalize(NormalizeUI):
    ''' --- IN YOUR NEW COPY AND PASTE FROM HERE --- '''
    def __init__(self, application, which = 'first', batch_mode = False):
            # Create references
        self.app = application
        self.master = self.app.mainwindow
        self.eleana = self.app.eleana
        self.grapher = self.app.grapher
        self.which = which
            # Create batch mode state
        self.batch = batch_mode
        # Do not build window if batch mode is true
        if not self.batch:
            super().__init__(self.master)
            # Create observer
        self.observer = Observer(self.eleana, self)
            # Initialize data to modify
        self.get_data(start=True)
            # Set current position in Results Dataset
        self.result_index = len(self.eleana.results_dataset)
        self.eleana.notify_on = True
        self.configure_window()

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

    def get_data(self, start = False):
        ''' Makes a copy of the selected data
            and stores it in self.original_data.
            You may perform calculations on self.original_data
        '''
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
        return True

    def ok_clicked(self, value):
        ''' Triggers 'perform_calculation' for the
            current data selected in first or second
            Name of this function must match the command in the button "OK"
        '''
        self.perform_calculation()

    def process_group(self):
        ''' Triggers 'perform_calculation' for all
            data in the current group.
            This should work without modifications
        '''
        self.mainwindow.config(cursor='watch')
        spectra = self.app.sel_first._values
        self.app.sel_first.set(spectra[0])
        self.eleana.selections[self.which] = 0
        for each in spectra:
            self.eleana.notify_on = True
            self.app.first_up_clicked()
            self.perform_calculations()
        self.mainwindow.config(cursor='')

    def configure_window(self):
        # YOU MUST MODIFY THIS METHOD ACCORDING
        # TO WHAT IS NEEDED

        # Configure Window
        self.mainwindow.title('Normalize amplitude')
        self.mainwindow.attributes('-topmost', False)

        # Replace tk Spinbox with CTkSpinbox
        self.spinboxFrame = self.builder.get_object('spinboxFrame', self.mainwindow)
        self.spinbox = self.builder.get_object('spinbox', self.mainwindow)
        self.spinbox.grid_remove()
        self.spinbox = CTkSpinbox(master=self.spinboxFrame, wait_for=0.01, command=self.ok_clicked, min_value=0,
                                  step_value=0.02, scroll_value=0.01, start_value=1)
        self.spinbox.grid(column=0, row=0, sticky='ew')

    ''' """""""""""""""""""""""""""""""""""""""""""""
                --- TO HERE --- 
    """""""""""""""""""""""""""""""""""""""""""""""""'''

    def perform_calculation(self):
        ''' Method that calculates something in your subprogram
            This must be prepared for a single data
            But you must check if it works for
            all possible data types
        '''
        normalize_to = float(self.spinbox.get())
        min = np.min(self.original_data.y)
        max = np.max(self.original_data.y)
        glob_min = np.min(min)
        glob_max = np.max(max)
        print(glob_min)
        print(glob_max)

if __name__ == "__main__":
    app = Normalize()
    app.run()
