#!/usr/bin/python3

import json
# Import Standard Python Modules
import pathlib
import customtkinter
import pygubu
from CTkMessagebox import CTkMessagebox
import sys
import customtkinter as ctk

# Import Eleana specific classes
from assets.general_eleana_methods import Eleana
from assets.menuActions import MenuAction
from assets.initialization import Init
from assets.graph_plotter import plotter
from assets.update_methods import Update
from assets.comboboxes_methods import Comboboxes

# -----GLOBAL VARIABLEs-------------
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui" / "Eleana_main.ui"
VERSION = 1
INTERPRETER = sys.executable  # <-- Python version for subprocesses

DEVEL = True

class EleanaMainApp:
    def __init__(self, eleana_instance, master=None):
        # Initialize eleana
        self.eleana = eleana_instance

        # START BUILDER
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("Eleana", master)
        self.mainwindow.iconify()
        self.mainwindow.withdraw()

        # Main menu
        _main_menu = builder.get_object("mainmenu", self.mainwindow)
        self.mainwindow.configure(menu=_main_menu)




        self.group_down = None
        self.group_up = None
        self.group = None
        self.first_down = None
        builder.connect_callbacks(self)
        # END OF PYGUBU BUILDER

        # Create references to Widgets and Frames
        self.sel_group = builder.get_object("sel_group", self.mainwindow)
        self.sel_first = builder.get_object("sel_first", self.mainwindow)
        self.sel_second = builder.get_object("sel_second", self.mainwindow)
        self.sel_result = builder.get_object("sel_result", self.mainwindow)
        self.firstFrame = builder.get_object("firstFrame", self.mainwindow)
        self.resultFrame = builder.get_object("resultFrame", self.mainwindow)
        self.resultStkFrame = builder.get_object("resultStkFrame", self.mainwindow)
        self.firstStkFrame = builder.get_object("firstStkFrame", self.mainwindow)
        self.secondStkFrame = builder.get_object("secondStkFrame", self.mainwindow)
        self.firstComplex = builder.get_object("firstComplex", self.mainwindow)
        self.secondComplex = builder.get_object("secondComplex", self.mainwindow)
        self.resultComplex = builder.get_object("resultComplex", self.mainwindow)
        self.graphFrame = builder.get_object('graphFrame', self.mainwindow)
        self.f_stk = builder.get_object('f_stk', self.mainwindow)
        self.s_stk = builder.get_object('s_stk', self.mainwindow)
        self.r_stk = builder.get_object('r_stk', self.mainwindow)
        self.btn_clear_results = builder.get_object('btn_clear_results', self.mainwindow)

        # Set default values
        self.firstComplex.set(value="re")
        self.secondComplex.set(value="re")
        self.resultComplex.set(value="re")
        self.legendFrame = builder.get_object('legendFrame', self.mainwindow)
        
    def run(self):
        self.mainwindow.deiconify()
        self.mainwindow.mainloop()

    def group_down_clicked(self):
        pass

    def group_up_clicked(self):
        pass

    def group_selected(self, value):
        pass

    def first_down_clicked(self):
        current_position = app.sel_first.get()
        list_of_items = app.sel_first._values
        if current_position == 'None':
            return
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_first not found')
            return

        try:
            new_position = list_of_items[index - 1]
            app.sel_first.set(new_position)
            self.first_selected(new_position)
        except IndexError:
            return



    def first_up_clicked(self):
        current_position = app.sel_first.get()
        list_of_items = app.sel_first._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_first not found.')
            return

        try:
            new_position = list_of_items[index+1]
            app.sel_first.set(new_position)
            self.first_selected(new_position)
        except IndexError:
            return



    def first_complex_clicked(self, value):
            eleana.selections['f_cpl'] = value
            after_selection('first')

    def first_selected(self, selected_value_text: str):
        if selected_value_text == 'None':
            eleana.selections['first'] = -1
            app.firstComplex.grid_remove()
            app.firstStkFrame.grid_remove()
            return
        i = 0
        while i < len(eleana.dataset):
            name = eleana.dataset[i].name_nr
            if name == selected_value_text:
                eleana.selections['first'] = i
                break
            i += 1

        update.list_in_combobox(app, eleana, 'sel_first')
        update.list_in_combobox(app, eleana, 'f_stk')

        if eleana.dataset[eleana.selections['first']].complex:
            app.firstComplex.grid()
        else:
            app.firstComplex.grid_remove()
    def f_stk_selected(self, selected_value_text):
        if selected_value_text in app.f_stk._values:
            index = app.f_stk._values.index(selected_value_text)

        eleana.selections['f_stk'] = index

    def f_stk_up_clicked(self):
        current_position = app.f_stk.get()
        list_of_items = app.f_stk._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in f_stk not found.')
            return

        try:
            new_position = list_of_items[index + 1]
            app.f_stk.set(new_position)
            eleana.selections['f_stk'] = index +1
        except IndexError:
            return

    def f_stk_down_clicked(self):
        current_position = app.f_stk.get()
        list_of_items = app.f_stk._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in f_stk not found.')
            return
        if index == 0:
            return
        try:
            new_position = list_of_items[index - 1]
            app.f_stk.set(new_position)
            eleana.selections['f_stk'] = index - 1
        except IndexError:
            return

    def second_selected(self, selected_value_text):
        if selected_value_text == 'None':
            eleana.selections['second'] = -1
            app.secondComplex.grid_remove()
            app.secondStkFrame.grid_remove()
            return
        i = 0
        while i < len(eleana.dataset):
            name = eleana.dataset[i].name_nr
            if name == selected_value_text:
                eleana.selections['second'] = i
                break
            i += 1

        update.list_in_combobox(app, eleana, 'sel_second')
        update.list_in_combobox(app, eleana, 's_stk')

        if eleana.dataset[eleana.selections['second']].complex:
            app.secondComplex.grid()
        else:
            app.secondComplex.grid_remove()
    def second_down_clicked(self):
        current_position = app.sel_second.get()
        list_of_items = app.sel_second._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_second not found.')
            return

        if index <= 0:
            return

        try:
            new_position = list_of_items[index - 1]
            app.sel_second.set(new_position)
            self.second_selected(new_position)
        except IndexError:
            return


    def second_up_clicked(self):
        current_position = app.sel_second.get()
        list_of_items = app.sel_second._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_second not found.')
            return

        try:
            new_position = list_of_items[index + 1]
            app.sel_second.set(new_position)
            self.second_selected(new_position)
        except IndexError:
            return

    def s_stk_selected(self, selected_value_text):
        if selected_value_text in app.s_stk._values:
            index = app.s_stk._values.index(selected_value_text)

        eleana.selections['s_stk'] = index

    def s_stk_up_clicked(self):
        current_position = app.s_stk.get()
        list_of_items = app.s_stk._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in s_stk not found.')
            return

        try:
            new_position = list_of_items[index + 1]
            app.s_stk.set(new_position)
            eleana.selections['s_stk'] = index +1
        except IndexError:
            return

    def s_stk_down_clicked(self):
        current_position = app.s_stk.get()
        list_of_items = app.s_stk._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in s_stk not found.')
            return
        if index == 0:
            return
        try:
            new_position = list_of_items[index - 1]
            app.s_stk.set(new_position)
            eleana.selections['s_stk'] = index - 1
        except IndexError:
            return


    def second_complex_clicked(self, value):
            eleana.selections['s_cpl'] = value
            after_selection('second')
    def swap_first_second(self):
        first_pos = app.sel_first.get()
        second_pos = app.sel_second.get()
        first_stk = app.f_stk.get()
        second_stk = app.s_stk.get()

        if first_pos == 'None':
            app.firstComplex.grid_remove()

        if first_pos == 'None':
            app.secondComplex.grid_remove()


        app.sel_first.set(second_pos)
        app.sel_second.set(first_pos)

        self.first_selected(second_pos)
        self.second_selected(first_pos)

        app.f_stk.set(second_stk)
        app.s_stk.set(first_stk)

        self.f_stk_selected(second_stk)
        self.s_stk_selected(first_stk)


    def second_to_result(self):
        current = app.sel_second.get()
        if current == 'None':
            return
        index = get_index_by_name(current)
        spectrum = eleana.dataset[index]

        # Check the name if the same already exists in eleana.result_dataset
        list_of_results = []
        for each in eleana.results_dataset:
            list_of_results.append(each.name)

        if spectrum.name in list_of_results:
            dialog = customtkinter.CTkInputDialog(
                text="There is data with the same name. Please enter a different name.", title="Enter new name")
            input = dialog.get_input()
            if type(input) == str and spectrum.name != input:
                spectrum.name = input
            else:
                return

        # Send to result and update lists
        eleana.results_dataset.append(spectrum)
        update.list_in_combobox(app, eleana, 'sel_result')
        update.list_in_combobox(app, eleana, 'r_stk')

        # Set the position to the last added item
        list = app.sel_result._values
        position = list[-1]
        app.sel_result.set(position)


    def result_selected(self, selected_value_text):
        if selected_value_text == 'None':
            eleana.selections['result'] = -1
            app.resultComplex.grid_remove()
            app.resultStkFrame.grid_remove()
            return

        i = 0
        while i < len(eleana.results_dataset):
            name = eleana.results_dataset[i].name
            if name == selected_value_text:
                eleana.selections['result'] = i
                break
            i += 1

        update.list_in_combobox(app, eleana, 'sel_result')
        update.list_in_combobox(app, eleana, 'r_stk')

        if eleana.results_dataset[eleana.selections['result']].complex:
            app.resultComplex.grid()
        else:
            app.resultComplex.grid_remove()


    def result_up_clicked(self):
        current_position = app.sel_result.get()
        list_of_items = app.sel_result._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_result not found.')
            return

        try:
            new_position = list_of_items[index + 1]
            app.sel_result.set(new_position)
            self.result_selected(new_position)
        except IndexError:
            return

    def result_down_clicked(self):
        current_position = app.sel_result.get()
        list_of_items = app.sel_result._values
        if current_position == 'None':
            return
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_first not found')
            return

        try:
            new_position = list_of_items[index - 1]
            app.sel_result.set(new_position)
            self.result_selected(new_position)
        except IndexError:
            return

    def r_stk_up_clicked(self):
        current_position = app.r_stk.get()
        list_of_items = app.r_stk._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in r_stk not found.')
            return

        try:
            new_position = list_of_items[index + 1]
            app.r_stk.set(new_position)
            eleana.selections['r_stk'] = index + 1
        except IndexError:
            return


    def r_stk_down_clicked(self):
        current_position = app.r_stk.get()
        list_of_items = app.r_stk._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in r_stk not found.')
            return
        if index == 0:
            return
        try:
            new_position = list_of_items[index - 1]
            app.r_stk.set(new_position)
            eleana.selections['r_stk'] = index - 1
        except IndexError:
            return


    def first_to_result(self):
            current = app.sel_first.get()
            if current == 'None':
                return
            index = get_index_by_name(current)
            spectrum = eleana.dataset[index]

            # Check the name if the same already exists in eleana.result_dataset
            list_of_results = []
            for each in eleana.results_dataset:
                list_of_results.append(each.name)

            if spectrum.name in list_of_results:
                dialog = ctk.CTkInputDialog(text="There is data with the same name. Please enter a different name.", title="Enter new name")
                input = dialog.get_input()
                if type(input) == str and spectrum.name != input:
                    spectrum.name = input
                else:
                    return

            # Send to result and update lists
            eleana.results_dataset.append(spectrum)
            update.list_in_combobox(app, eleana, 'sel_result')
            update.list_in_combobox(app, eleana, 'r_stk')

            # Set the position to the last added item
            list = app.sel_result._values
            position = list[-1]
            app.sel_result.set(position)
            if spectrum.complex:
                app.resultComplex.grid()
            else:
                app.resultComplex.grid_remove()

    def clear_results(self):
        quit_dialog = CTkMessagebox(title="Clear results", message="Are you sure you want to clear the entire dataset in the results?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = quit_dialog.get()
        if response == "Yes":
            eleana.results_dataset = []
            app.sel_result.configure(values = ['None'])
            app.r_stk.configure(values = [])
            app.resultFrame.grid_remove()

    def clear_dataset(self):
        quit_dialog = CTkMessagebox(title="Clear dataset",
                                    message="Are you sure you want to clear the entire dataset?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = quit_dialog.get()
        if response == "Yes":
            init.main_window(app, eleana)
            app.resultFrame.grid_remove()
            app.firstComplex.grid_remove()
            app.firstStkFrame.grid_remove()
            app.secondComplex.grid_remove()
            app.secondStkFrame.grid_remove()


    ''' 
    FUNCTIONS ACTIVATED BY MAIN MENU SELECTION
    '''

    # FILE
    # --- Load Project
    def load_project(self):
        project = menuAction.load_project(eleana)

        eleana.selections = project['selections']
        eleana.dataset = project['dataset']
        eleana.results_dataset = project['results_dataset']
        eleana.assignmentToGroups = project['assignmentToGroups']
        eleana.groupsHierarchy = project['groupsHierarchy']
        eleana.notes = project['notes']
        eleana.paths = project['paths']

        update.dataset_list(eleana)
        update.all_lists(app, eleana)

        selected_value_text = eleana.dataset[eleana.selections['first']].name_nr
        self.first_selected(selected_value_text)
        app.sel_first.set(selected_value_text)

        selected_value_text = eleana.dataset[eleana.selections['second']].name_nr
        self.second_selected(selected_value_text)
        app.sel_second.set(selected_value_text)

        selected_value_text = eleana.dataset[eleana.selections['result']].name_nr
        self.result_selected(selected_value_text)
        app.sel_result.set(selected_value_text)

    # --- Save as
    def save_as(self):
        report = menuAction.save_as(eleana)

        if report['error']:
            CTkMessagebox(title="Error", message=report['desc'], icon="cancel")
        else:
            last_projects = eleana.paths['last_projects']
            last_projects.insert(0, report['return'].name)

        # Remove duplications and limit the list to 10 items
        last_projects= list(set(last_projects))
        last_projects = [element for i, element in enumerate(last_projects) if i <= 10]

        # Write the list to eleana.paths
        eleana.paths['last'] = last_projects

        # Perform uprade to place the item into menu
        update.last_projects_menu(app, eleana)

    # --- Import EPR --> Bruker Elexsys

    def import_elexsys(self):
        ''' Open window that loads the spectra '''
        menuAction.loadElexsys(eleana)

        update.dataset_list(eleana)
        update.all_lists(app, eleana)

    # --- Quit (also window close by clicking on X)
    def close_application(self):
        quit_dialog = CTkMessagebox(title="Quit", message="Do you want to close the program?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = quit_dialog.get()
        if response == "Yes":
            app.mainwindow.iconify()
            app.mainwindow.destroy()

    # EDIT Menu:
    #   Notes
    def notes(self):
        filename = menuAction.notes()
        # Grab result
        file_back = eleana.read_tmp_file(filename)
        eleana.notes = json.loads(file_back)

# --- GENERAL BATCH METHODS ---



def after_import(app, eleana):
    # Update dataset (names, groups and groups assignment)
    update.dataset_list(eleana)

    # Update combobox lists
    update.all_lists(app, eleana)

def get_index_by_name(selected_value_text):
    ''' Function returns index in dataset of spectrum
        having the name_nr '''
    i = 0
    while i < len(eleana.dataset):
        name = eleana.dataset[i].name_nr
        if name == selected_value_text:
            return i
        i += 1


'''Create main instances 
app     - object of the main window containing GUI and tkinter and ctk widgets
eleana  - object containing base variables that store all information and dataset 
          that are available everywhere in the application.
menuAction - object containing methods to handle selections of items in the program menu
update  - object containing methods for refreshing GUI, creating lists in comboboxes etc
comboboxLists - methods for creating list, picking, setting items etc. They do not change GUI elements.
init    - object that is used to initialize program on start 
'''

ctk.set_appearance_mode("dark")

eleana = Eleana()
app = EleanaMainApp(eleana)


menuAction = MenuAction()
update = Update()
comboboxes = Comboboxes()
init = Init(app, eleana)

# Set geometry, icon and default combobox values
init.main_window(app, eleana)

init.folders()



update.gui_widgets(app, eleana, comboboxes)
#dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
#print(dialog.get_input())
# Run
if __name__ == "__main__":
    app.run()
