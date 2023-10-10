#!/usr/bin/python3

import json
# Import Standard Python Modules
import pathlib
import customtkinter

from CTkMessagebox import CTkMessagebox
import sys


# Import Eleana specific classes


from ui.gui_builder import *
from assets.general_eleana_methods import Eleana
from assets.menuActions import MenuAction
from assets.initialization import Init
from assets.graph_plotter import plotter

# -----GLOBAL VARIABLEs-------------

VERSION = 1
INTERPRETER = sys.executable  # <-- Python version for subprocesses

DEVEL = True

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui" / "Eleana_main.ui"

class EleanaMainApp:
    def __init__(self, master=None):
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
        first_down_clicked()

    def first_up_clicked(self):
        first_up_clicked(self)

    def first_complex_clicked(self, value):
        first_complex_clicked(value)

    def first_selected(self, selected_value_text: str):
        first_selected(selected_value_text)

    def f_stk_selected(self, selected_value_text):
        f_stk_selected(selected_value_text)

    def f_stk_up_clicked(self):
        f_stk_up_clicked()

    def f_stk_down_clicked(self):
        f_stk_down_clicked()

    def second_selected(self, selected_value_text):
        second_selected(selected_value_text)

    def second_down_clicked(self):
        second_down_clicked()

    def second_up_clicked(self):
        second_up_clicked()

    def s_stk_selected(self, selected_value_text):
        s_stk_selected(selected_value_text)

    def s_stk_up_clicked(self):
        s_stk_up_clicked()

    def s_stk_down_clicked(self):
        s_stk_down_clicked()

    def second_complex_clicked(self, value):
        second_complex_clicked(value)

    def swap_first_second(self):
        swap_first_second()

    def second_to_result(self):
        second_to_result()

    def result_selected(self, selected_value_text):
        result_selected(selected_value_text)

    def result_up_clicked(self):
        result_up_clicked()

    def result_down_clicked(self):
        result_down_clicked()

    def first_to_result(self):
        first_to_result()

    def load_project(self):
        load_project()

    def save_as(self):
        save_as()

    def import_elexsys(self):
        import_elexsys()

    # --- Quit (also window close by clicking on X)
    def close_application(self):
        close_application()

    def notes(self):
        notes()


# --- GENERAL BATCH METHODS ---
def group_down_clicked(self):
    pass


def group_up_clicked(self):
    pass


def group_selected(self, value):
    pass

def first_complex_clicked(value):
    print(value)
def first_down_clicked(self):
    ''' POPRAWIONE '''
    current_val = comboboxes.get_current_position(app, eleana, 'sel_first')

    new_index = current_val['index_on_list'] - 1
    if new_index <= 0:
        eleana.selections['first'] = -1
        comboboxes.set_on_position_value(app, eleana, 'sel_first', 'None')
        update.gui_widgets(app, eleana, comboboxes)
        plotter(app, eleana, comboboxes)
        return
    elif new_index > current_val['last_index_on_list']:
        return
    else:
        comboboxes.set_on_position_index(app, eleana, 'sel_first', new_index)
        new_value = comboboxes.get_current_position(app, eleana, 'sel_first')
        index_in_eleana = eleana.name_nr_to_index(new_value['value'])
        eleana.selections['first'] = index_in_eleana
    after_selection('first')

    '''-----------------------------
    DISPLAY INFORMATION FOR DEBUG
    --------------------------------'''
    if DEVEL:
        test_variables()
    '''-----------------------------'''


def first_up_clicked(self):
    ''' POPRAWIONE '''
    current_val = comboboxes.get_current_position(app, eleana, 'sel_first')

    new_index = current_val['index_on_list'] + 1
    # if new_index == 0:
    #     eleana.selections['first'] = -1
    #     comboboxes.set_on_position_value(app, eleana, 'sel_first', 'None')
    if new_index > current_val['last_index_on_list']:
        return
    else:
        comboboxes.set_on_position_index(app, eleana, 'sel_first', new_index)
        new_value = comboboxes.get_current_position(app, eleana, 'sel_first')
        index_in_eleana = eleana.name_nr_to_index(new_value['value'])
        eleana.selections['first'] = index_in_eleana

    after_selection('first')

    '''-----------------------------
    DISPLAY INFORMATION FOR DEBUG
    --------------------------------'''
    if DEVEL:
        test_variables()
    '''-----------------------------'''

    def first_complex_clicked(self, value):
        eleana.selections['f_cpl'] = value
        after_selection('first')


def first_selected(self, selected_value_text: str):
    ''' POPRAWIONE '''
    if selected_value_text == 'None':
        eleana.selections['first'] = -1

    after_selection('first')


def f_stk_selected(self, selected_value_text):
    ''' POPRAWIONE '''
    comboboxes.set_on_position_value(app, eleana, 'f_stk', selected_value_text)
    current_value = comboboxes.get_current_position(app, eleana, 'f_stk')
    eleana.selections['f_stk'] = current_value['index_on_list']

    after_selection('first')


def f_stk_up_clicked(self):
    ''' POPRAWIONE '''
    current_val = comboboxes.get_current_position(app, eleana, 'f_stk')
    new_index = current_val['index_on_list'] + 1
    if new_index > current_val['last_index_on_list']:
        return
    else:
        comboboxes.set_on_position_index(app, eleana, 'f_stk', new_index)
        eleana.selections['f_stk'] = new_index

    after_selection('first')


def f_stk_down_clicked(self):
    # ''' POPRAWIONE '''
    current_val = comboboxes.get_current_position(app, eleana, 'f_stk')
    new_index = current_val['index_on_list'] - 1
    if new_index < 0:
        return
    else:
        comboboxes.set_on_position_index(app, eleana, 'f_stk', new_index)
        eleana.selections['f_stk'] = new_index

    after_selection('first')


def second_selected(self, selected_value_text):
    ''' POPRAWIONE '''
    if selected_value_text == 'None':
        eleana.selections['second'] = -1
    after_selection('second')


def second_down_clicked(self):
    current_val = comboboxes.get_current_position(app, eleana, 'sel_second')
    new_index = current_val['index_on_list'] - 1
    if new_index <= 0:
        eleana.selections['second'] = -1
        comboboxes.set_on_position_value(app, eleana, 'sel_second', 'None')
        update.gui_widgets(app, eleana, comboboxes)
        plotter(app, eleana, comboboxes)
        return
    elif new_index > current_val['last_index_on_list']:
        return
    else:
        comboboxes.set_on_position_index(app, eleana, 'sel_second', new_index)
        new_value = comboboxes.get_current_position(app, eleana, 'sel_second')
        index_in_eleana = eleana.name_nr_to_index(new_value['value'])
        eleana.selections['second'] = index_in_eleana
    after_selection('second')


def second_up_clicked(self):
    current_val = comboboxes.get_current_position(app, eleana, 'sel_second')
    new_index = current_val['index_on_list'] + 1

    if new_index > current_val['last_index_on_list']:
        return
    else:
        comboboxes.set_on_position_index(app, eleana, 'sel_second', new_index)
        new_value = comboboxes.get_current_position(app, eleana, 'sel_second')
        index_in_eleana = eleana.name_nr_to_index(new_value['value'])
        eleana.selections['second'] = index_in_eleana

    after_selection('second')


def s_stk_selected(self, selected_value_text):
    comboboxes.set_on_position_value(app, eleana, 's_stk', selected_value_text)
    current_value = comboboxes.get_current_position(app, eleana, 's_stk')
    eleana.selections['s_stk'] = current_value['index_on_list']

    after_selection('second')


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
    first, first_stk, f_cpl = eleana.selections['first'], eleana.selections['f_stk'], eleana.selections['f_cpl']
    second, second_stk, s_cpl = eleana.selections['second'], eleana.selections['s_stk'], eleana.selections['s_cpl']

    eleana.selections['first'] = second
    eleana.selections['f_stk'] = second_stk
    eleana.selections['f_cpl'] = s_cpl

    eleana.selections['second'] = first
    eleana.selections['s_stk'] = first_stk
    eleana.selections['s_cpl'] = f_cpl

    pos_first = comboboxes.get_current_position(app, eleana, 'sel_first')
    pos_first_stk = comboboxes.get_current_position(app, eleana, 'f_stk')

    pos_second = comboboxes.get_current_position(app, eleana, 'sel_second')
    pos_second_stk = comboboxes.get_current_position(app, eleana, 's_stk')

    comboboxes.set_on_position_value(app, eleana, 'sel_second', pos_first['value'])
    comboboxes.set_on_position_value(app, eleana, 'sel_first', pos_second['value'])
    pos_first = comboboxes.get_current_position(app, eleana, 'sel_first')
    pos_second = comboboxes.get_current_position(app, eleana, 'sel_second')

    try:
        pos_first_stk = comboboxes.get_current_position(app, eleana, 'f_stk')
        pos_second_stk = comboboxes.get_current_position(app, eleana, 's_stk')
        comboboxes.set_on_position_value(app, eleana, 's_stk', pos_first_stk['value'])
        comboboxes.set_on_position_value(app, eleana, 'f_stk', pos_second_stk['value'])
    except:
        pass

    after_selection('first')
    after_selection('second')


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
        current = comboboxes.get_current_position(app, eleana, 'sel_result')

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
    comboboxes.set_on_position_index(app, eleana, 'sel_result', current + 1)
    update.gui_widgets(app, eleana, comboboxes)


def result_down_clicked(self):
    current = eleana.selections['result']
    if current == -1:
        current = -1
    else:
        current = current - 1

    eleana.selections['result'] = current
    comboboxes.set_on_position_index(app, eleana, 'sel_result', current + 1)
    update.gui_widgets(app, eleana, comboboxes)


def first_to_result(self):
    # If FIRST is set to none then return
    if eleana.selections['first'] < 0:
        return

    # Copy current data to data_to_result
    data_in_first = eleana.dataset[eleana.selections['first']]

    # Get all names from results dataset
    names_in_result_dataset = []

    for each in eleana.results_dataset:
        names_in_result_dataset.append(each.name)

    # Check if the same nas as in FIRST exists in dataset
    if data_in_first.name in names_in_result_dataset:
        dialog = customtkinter.CTkInputDialog(
            text="There is data with the same name. Please enter a different name.", title="Enter new name")
        input = dialog.get_input()

        if type(input) == str:
            data_in_first.name = input
        else:
            return

    print(app.sel_first["values"])
    # Write the same name to name_nr (without number)
    data_in_first.name_nr = data_in_first.name

    after_selection('first')
    after_selection('second')

    '''-----------------------------
    DISPLAY INFORMATION FOR DEBUG
    --------------------------------'''
    if DEVEL:
        test_variables()
    '''-----------------------------'''
    # Add to eleana.results_dataset
    # eleana.results_dataset.append(data_in_first)

    # update.combobox_all_lists(app, eleana)
    # comboboxes.populate_lists(app, eleana)

    # self.result_selected(data_in_first.name_nr)
    # if data_in_first.type == 'stack 2D':
    #     comboboxes.set_on_position_index(app, eleana, 'r_stk', 0)
    #
    # after_selection('first')
    # after_selection('second')
    # after_selection('result')

    # comboboxes.set_on_position_value(app, eleana,'sel_result',data_in_first.name_nr)
    # #
    # # first.name_nr = input
    # eleana.results_dataset.append(first)
    # index = len(eleana.results_dataset) - 1
    # eleana.selections['result'] = index
    # eleana.selections['r_stk'] = 0
    #
    # after_selection('result')
    # new_position = eleana.combobox_lists['sel_result']
    # new_val = new_position[-1]
    # comboboxes.set_on_position_value(app, eleana, 'sel_result', new_val)


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
    import_elexsys()


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


def after_data_load(ref_to_eleana):
    # Create numbered names
    dataset = ref_to_eleana.dataset

    i = 0
    while i < len(dataset):
        name = dataset[i].name
        dataset[i].name_nr = str(i) + '. ' + name

    ref_to_eleana.dataset = dataset
    return ref_to_eleana
def import_elexsys():
    new_dataset = menuAction.loadElexsys(eleana.dataset, eleana.paths['last_import_dir'])
    eleana.dataset = new_dataset




''' START PROCEURES '''
customtkinter.set_appearance_mode("dark")
app = EleanaMainApp()
eleana = Eleana()
menuAction = MenuAction()
# update = Update()
# comboboxes = Comboboxes()
init = Init()

# Set geometry, icon and default combobox values
init.main_window(app, eleana)


init.folders(eleana)


#update.gui_widgets(app, eleana, comboboxes)
#dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
#print(dialog.get_input())
# Run
if __name__ == "__main__":
    app.run()
