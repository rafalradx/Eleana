#!/usr/bin/python3
import copy
import pathlib
import pygubu
import tkinter as tk
from assets.Observer import Observer
from modules.CTkMessagebox import CTkMessagebox
from assets.Sounds import Sound
from CTkSpinbox import CTkSpinbox
#from subprogs.progress_bar.progress_bar import ProgressBar
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "modify.ui"

from Observer import Observer

class ModifyData:
    def __init__(self, references, which = 'first'): # instances master, eleana=None, grapher=None, app=None ):
        # References to the main objects
        self.which = which
        self.app = references
        self.eleana = self.app.eleana
        self.grapher = self.app.grapher
        self.master = self.app.mainwindow
        self.sound = Sound()

        # Build GUI
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        # Configure main window
        self.mainwindow = builder.get_object("toplevel1", self.master)
        self.mainwindow.title("Modify")
        self.mainwindow.attributes('-topmost', True)
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.cancel)

        # References to widgets
        self.sel_x_oper = builder.get_object("sel_x_oper", self.master)
        self.sel_y_oper = builder.get_object("sel_y_oper", self.master)
        self.sel_z_oper = builder.get_object("sel_z_oper", self.master)
        self.x_axisFrame = builder.get_object("xaxisFrema", self.master)
        self.y_axisFrame = builder.get_object("ctkframe14", self.master)
        self.z_axisFrame = builder.get_object("ctkframe17", self.master)

        self.spinbox_x = builder.get_object("spinbox_x", self.master)
        self.spinbox_y = builder.get_object("spinbox_y", self.master)
        self.spinbox_z = builder.get_object("spinbox_z", self.master)
        self.processFrame = builder.get_object("processFrame", self.master)
        self.processFrame.grid_remove()
        self.progress_bar = builder.get_object("progress_bar", self.master)

        self.spinbox_x.grid_remove()
        self.spinbox_y.grid_remove()
        self.spinbox_z.grid_remove()
        # Configure spinbox validation
        # self.spinbox_x.configure(validate='key', validatecommand=(self.master.register(self.validate_spinbox), '%P'))
        # self.spinbox_y.config(validate='key', validatecommand=(self.master.register(self.validate_spinbox), '%P'))
        # self.spinbox_z.config(validate='key', validatecommand=(self.master.register(self.validate_spinbox), '%P'))

        self.spinbox_x = CTkSpinbox(self.x_axisFrame, command=self.ok_clicked)
        self.spinbox_x.grid(column = 0, row=3, sticky="nsew", padx=5, pady=5)
        self.spinbox_y = CTkSpinbox(self.y_axisFrame, command=self.ok_clicked)
        self.spinbox_y.grid(column=0, row=3, sticky="nsew", padx=5, pady=5)
        self.spinbox_z = CTkSpinbox(self.z_axisFrame, command=self.ok_clicked)
        self.spinbox_z.grid(column=0, row=3, sticky="nsew", padx=5, pady=5)

        # Set comboboxes to None
        self.sel_x_oper.set("Add (+)")
        self.sel_y_oper.set("Subtract (-)")
        self.sel_z_oper.set("None")

        # References to radiobuttons
        self.r1 = builder.get_object("r1", self.master)
        self.r2 = builder.get_object("r2", self.master)
        self.r3 = builder.get_object("r3", self.master)
        self.r4 = builder.get_object("r4", self.master)
        self.r5 = builder.get_object("r5", self.master)
        self.r6 = builder.get_object("r6", self.master)
        self.r7 = builder.get_object("r7", self.master)
        self.r8 = builder.get_object("r8", self.master)
        self.r9 = builder.get_object("r9", self.master)

        # Radiobuttons variable
        self.step = tk.DoubleVar()
        builder.import_variables(self, ['step'])
        builder.connect_callbacks(self)

        # Set staring values for spinboxes
        self.set_spinbox_starting_value()
        self.r5.select()

        # Response to None
        self.response = None

        # Create observer
        self.observer = Observer(self.eleana, self)

        # Get data to modify
        self.get_data(start = True)

        # Switch off the batch mode
        self.batch = False

        # Set current position in Results Dataset
        self.result_index = len(self.eleana.results_dataset)

        self.eleana.notify_on = True
    ''' STANDARD METHODS TO HANDLE WINDOW BEHAVIOR '''
    def data_changed(self):
        print("Triggered by observer")
        # This is trigerred by the observer
        self.get_data()
        self.perform_calculations()

    def get(self):
        if self.mainwindow.winfo_exists():
           self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event = None):
    # Close the application
        self.response = None
        # Unregister observer
        self.eleana.detach(self.observer)
        self.mainwindow.destroy()

    def run(self):
        self.mainwindow.mainloop()

    ''' END OF STANDARD METHODS '''

    def set_step(self):
    # Set the step for spinbox according to the radio buttons
        current_step = self.step.get()
        self.spinbox_x.scroll_value = current_step
        self.spinbox_x.step_value = current_step

        self.spinbox_y.scroll_value = current_step
        self.spinbox_y.step_value = current_step

        self.spinbox_z.scroll_value = current_step
        self.spinbox_z.step_value = current_step

    #self.spinbox_y.config(increment=current_step)
        #self.spinbox_z.config(increment=current_step)

    def set_spinbox_starting_value(self):
    # Set default values in spinboxes
        self.spinbox_x.set(1)
        self.spinbox_y.set(1)
        self.spinbox_z.set(1)

    def ok_clicked(self, value = None):
        self.perform_calculations()
        self.grapher.plot_graph()

    def enter_pressed(self, event):
        x_val = self.spinbox_x.get()
        y_val = self.spinbox_y.get()
        z_val = self.spinbox_z.get()
        if event.keysym == 'Return' or event.keysym == 'KP_Enter':
            pass
        elif not event.char.isdigit():
            self.spinbox_x.set(x_val)
            self.spinbox_y.set(y_val)
            self.spinbox_z.set(z_val)

    def validate_spinbox(self, value):
        # Check if value in spinbox is a number
        try:
            if value == "":
                return True
            float(value)
            return True
        except ValueError:
            self.sound.beep()
            return False

    def get_data(self, start = False):
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

    def process_group(self):
        self.mainwindow.config(cursor='watch')
        spectra = self.app.sel_first._values
        self.app.sel_first.set(spectra[0])
        self.eleana.selections[self.which] = 0
        for each in spectra:
            self.eleana.notify_on = True
            self.app.first_up_clicked()
            self.perform_calculations()
        self.mainwindow.config(cursor='')

    def perform_calculations(self):
    # This function takes data from self.original_data and perform calculations
    # on X, Y and Z axis according to what is selected in GUI.
    # The effect of calculations is in self.modified_data
        x_oper = self.sel_x_oper.get()[:2]
        y_oper = self.sel_y_oper.get()[:2]
        z_oper = self.sel_z_oper.get()[:2]
        x_val = float(self.spinbox_x.get())
        y_val = float(self.spinbox_y.get())
        z_val = float(self.spinbox_z.get())

        # Operations on X axis
        if x_oper == 'Ad': # (+)
            self.result_data.x = self.original_data.x + x_val
        elif x_oper == 'Su': # (-)
            self.result_data.x = self.original_data.x - x_val
        elif x_oper == 'Mu': # (*)
            self.result_data.x = self.original_data.x * x_val
        elif x_oper == 'Di':  # (/)
            if x_val == 0:
                if not self.batch:
                    info = CTkMessagebox(title="Error", message="Cannot divide X axis by zero.", icon="cancel")
            else:
                self.result_data.x = self.original_data.x / x_val
        elif x_oper == 'Po':  # (^2)
            not_negative = np.all(self.original_data.x >= 0)
            if not_negative:
                self.result_data.x = self.original_data.x ** 2
            else:
                if not self.batch:
                    info = CTkMessagebox(title="Error", message="The X-axis contains negative values. It should not be raised to the second power.", icon="cancel")
        elif x_oper == 'Sq':  # (\/x)
            not_negative = np.all(self.original_data.x >= 0)
            if not_negative:
                self.result_data.x = self.original_data.x ** 0.5
            else:
                if not self.batch:
                    info = CTkMessagebox(title="Error", message="The X-axis contains negative values. Square root calculation is not possible.", icon="cancel")
        else:
            pass

        # Operations on Y axis
        if y_oper == 'Ad':  # (+)
            self.result_data.y = self.original_data.y + y_val
        elif y_oper == 'Su':  # (-)
            self.result_data.y = self.original_data.y - y_val
        elif y_oper == 'Mu':  # (*)
            self.result_data.y = self.original_data.y * y_val
        elif y_oper == 'Di':  # (/)
            if y_val == 0:
                if not self.batch:
                    info = CTkMessagebox(title="Error", message="Cannot divide Y axis by zero.", icon="cancel")
            else:
                self.result_data.y = self.original_data.y / y_val
        elif y_oper == 'Po':  # (^2)
            self.result_data.y = self.original_data.y ** 2
        elif y_oper == 'Sq':  # (\/x)
            not_negative = np.all(self.original_data.y >= 0)
            if not_negative:
                self.result_data.y = self.original_data.y ** 0.5
            else:
                if not self.batch:
                    info = CTkMessagebox(title="Error", message="The Y-axis contains negative values. Square root calculation is not possible.", icon="cancel")
        else:
            pass

        # Operations on Z
        if self.original_data.type == 'single 2D':
            pass
        elif z_oper == 'Ad':  # (+)
            self.result_data.z = self.original_data.z + z_val
        elif z_oper == 'Su':  # (-)
            self.result_data.z = self.original_data.z - z_val
        elif z_oper == 'Mu':  # (*)
            self.result_data.z = self.original_data.z * z_val
        elif z_oper == 'Di':  # (/)
            if z_val == 0:
                if not self.batch:
                    info = CTkMessagebox(title="Error", message="Cannot divide Z axis by zero.", icon="cancel")
            else:
                self.result_data.z = self.original_data.z / z_val
        elif z_oper == 'Po':  # (^2)
            self.result_data.z = self.original_data.z ** 2
        elif z_oper == 'Sq':  # (\/x)
            not_negative = np.all(self.original_data.z >= 0)
            if not_negative:
                self.result_data.z = self.original_data.z ** 0.5
            else:
                if not self.batch:
                    info = CTkMessagebox(title="Error", message="The Y-axis contains negative values. Square root calculation is not possible.", icon="cancel")
        else:
            pass

if __name__ == "__main__":
    app = ModifyData()
    app.run()
