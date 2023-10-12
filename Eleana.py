#!/usr/bin/python3

import json
# Import Standard Python Modules
import pathlib
import customtkinter
import pygubu
from CTkMessagebox import CTkMessagebox
import sys


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

        # Set default values
        self.firstComplex.set(value="re")
        self.secondComplex.set(value="re")
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
            print('Cannot switch spectrum to higher')
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
            print('Cannot switch spectrum to higher')
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

        i = 0
        while i < len(eleana.dataset):
            name = eleana.dataset[i].name_nr
            if name == selected_value_text:
                eleana.selections['first'] = i
                break
            i += 1

        update.all_lists(app,eleana)


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
            print('Cannot switch spectrum to higher')
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
            print('Cannot switch spectrum to higher')
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

        i = 0
        while i < len(eleana.dataset):
            name = eleana.dataset[i].name_nr
            if name == selected_value_text:
                eleana.selections['second'] = i
                break
            i += 1

        update.all_lists(app, eleana)

    def second_down_clicked(self):
        current_position = app.sel_second.get()
        list_of_items = app.sel_second._values

        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Cannot switch spectrum to higher')
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
            print('Cannot switch spectrum to higher')
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
        ''' POPRAWIONE '''
        current_val = comboboxes.get_current_position(app, eleana, 's_stk')
        new_index = current_val['index_on_list'] + 1
        if new_index > current_val['last_index_on_list']:
            return
        else:
            comboboxes.set_on_position_index(app, eleana, 's_stk', new_index)
            eleana.selections['s_stk'] = new_index

        after_selection('second')

    def s_stk_down_clicked(self):
         # ''' POPRAWIONE '''
        current_val = comboboxes.get_current_position(app, eleana, 's_stk')
        new_index = current_val['index_on_list'] - 1
        if new_index < 0:
            return
        else:
            comboboxes.set_on_position_index(app, eleana, 's_stk', new_index)
            eleana.selections['s_stk'] = new_index

        after_selection('second')

    def second_complex_clicked(self, value):
            eleana.selections['s_cpl'] = value
            after_selection('second')
    def swap_first_second(self):
        pass

    def second_to_result(self):
        index = eleana.selections['second']
        if index == -1:
            return
        first = eleana.dataset[index]
        eleana.results_dataset.append(first)
        index = len(eleana.results_dataset) - 1
        eleana.selections['result'] = index
        eleana.selections['r_stk'] = 0

        after_selection('result')
        new_position = eleana.combobox_lists['sel_result']
        new_val = new_position[-1]
        comboboxes.set_on_position_value(app, eleana, 'sel_result', new_val)


    def result_selected(self, selected_value_text):
        if selected_value_text == 'None':
            eleana.selections['result'] = -1
        try:

            comboboxes.set_on_position_value(app, eleana, 'sel_result', selected_value_text)
            current = comboboxes.get_current_position(app,eleana, 'sel_result')

            eleana.selections['result'] = current['index_dataset']
        except:
            pass
        update.gui_widgets(app, eleana, comboboxes)



    def result_up_clicked(self):
        current = eleana.selections['result']
        current += 1
        if current == 0:
            current += 1
        if current > len(eleana.results_dataset):
            return

        eleana.selections['result'] = current
        comboboxes.set_on_position_index(app, eleana, 'sel_result', current+1)
        update.gui_widgets(app, eleana, comboboxes)

    def result_down_clicked(self):
        current = eleana.selections['result']
        if current == -1:
            current = -1
        else:
            current = current -1

        eleana.selections['result'] = current
        comboboxes.set_on_position_index(app, eleana, 'sel_result', current+1)
        update.gui_widgets(app, eleana, comboboxes)

    def first_to_result(self):


        #Check if the same nas as in FIRST exists in dataset
        if data_in_first.name in names_in_result_dataset:
            dialog = customtkinter.CTkInputDialog(
                text="There is data with the same name. Please enter a different name.", title="Enter new name")
            input = dialog.get_input()

            if type(input) == str:
                data_in_first.name = input
            else:
                return


    # Functions triggered by Menu selections
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
        after_import(app, eleana)

    # --- Save as
    def save_as(self):
        menuAction.save_as(eleana)

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

def after_selection(which):
    # Create references to widgets id in GUI
    if which == 'first':
        combobox_main = 'sel_first'
        combobox_stk = 'f_stk'
    elif which == 'second':
        combobox_main = 'sel_second'
        combobox_stk = 's_stk'
    elif which == 'result' or which=='r_stk':
        combobox_main = 'sel_result'



    #  Plot graph
    plotter(app, eleana, comboboxes)


'''Create main instances 
app     - object of the main window containing GUI and tkinter and ctk widgets
eleana  - object containing base variables that store all information and dataset 
          that are available everywhere in the application.
menuAction - object containing methods to handle selections of items in the program menu
update  - object containing methods for refreshing GUI, creating lists in comboboxes etc
comboboxLists - methods for creating list, picking, setting items etc. They do not change GUI elements.
init    - object that is used to initialize program on start 
'''

customtkinter.set_appearance_mode("dark")

eleana = Eleana()
app = EleanaMainApp(eleana)


menuAction = MenuAction()
update = Update()
comboboxes = Comboboxes()
init = Init()

# Set geometry, icon and default combobox values
init.main_window(app, eleana)

init.folders(eleana)



update.gui_widgets(app, eleana, comboboxes)
#dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
#print(dialog.get_input())
# Run
if __name__ == "__main__":
    app.run()
