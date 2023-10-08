#!/usr/bin/python3

import json
# Import Standard Python Modules
import pathlib
import customtkinter
import pygubu
from CTkMessagebox import CTkMessagebox

# Import Eleana specific classes
from assets.general_eleana_methods import Eleana, Update, Comboboxes
from assets.gui_actions.menu_actions import MenuAction
from assets.initialization import Init
from assets.graph_plotter import plotter
# ------------------
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui" / "Eleana_main.ui"

DEVEL = True

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


    def first_to_result(self):
        '''

        Tu jest problem, że po kliknieciu to reults przestaja działać przyciski first_up i first_down



        :return:
        '''
        index = eleana.selections['first']
        if index == -1:
            return
        first = eleana.dataset[index]
        first.name_nr = first.name
        if first.name_nr in eleana.combobox_lists['sel_result']:
            dialog = customtkinter.CTkInputDialog(text="There is data with the same name. Please enter a different name.", title="Enter new name")
            input = dialog.get_input()

            if type(input) == str:
                name = input
            else:
                return
        #
        # first.name_nr = input
        eleana.results_dataset.append(first)
        index = len(eleana.results_dataset) - 1
        eleana.selections['result'] = index
        eleana.selections['r_stk'] = 0

        after_selection('result')
        new_position = eleana.combobox_lists['sel_result']
        new_val = new_position[-1]
        comboboxes.set_on_position_value(app, eleana, 'sel_result', new_val)

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
        menuAction.loadElexsys()
        after_import(app, eleana)

        ''' When import is done and spectra in eleana.dataset[]
            it is needed to:

             1. Get list of spectra to put in the combobox list
                    entries = update.dataset_list()

             2. Create lists of coboboxes lists (not widgets)
                    comboboxList.create_all_lists(app)

             3. Put the lists created in p. 2 into widgets:
                    update.first(app, entries)
                    update.second(app, entires)

        '''

        # # Będę musiał dodać funkcję sprawdzenia grupy wewnątrz update.dataset_list
        # if eleana.selections['group'] == 'All':
        #     update.dataset_list(eleana)
        #     comboboxLists.create_all_lists(app, eleana)

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
    # Update dataset
    update.dataset_list(eleana)

    # Update lists that can be inserted to comboboxes
    update.combobox_all_lists(app, eleana)

    # Write list from eleana.comboboxlists to GUI widgets
    comboboxes.populate_lists(app, eleana)

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
        # Get index of data selected in eleana.result_dataset

        # Save current value in eleana.selections
        index_in_result_dataset = eleana.selections['result']
        comboboxes.set_on_position_index(app, eleana, 'sel_result', index_in_result_dataset+1)

        index = eleana.selections['r_stk']

        # 1. Display neccessary widgets and hide unused
        update.gui_widgets(app, eleana, comboboxes)
        # 2. Create list that will be pushed to combobox widgets
        update.combobox_create_list(app, eleana, 'sel_result')
        # 3. Put list into widgets
        comboboxes.populate_lists(app, eleana)

        # 4. Set combobox result to index:
        comboboxes.set_on_position_index(app, eleana, 'sel_result', index + 1)

        # 5. Check if STK Names should be added
        if eleana.results_dataset[index].type == 'stack 2D':
            update.combobox_create_list(app, eleana, 'r_stk')
            comboboxes.populate_lists(app, eleana)
            comboboxes.set_on_position_index(app, eleana, 'r_stk', 0)
        return
    else:
        print('Wrong parameter "which" in after_selection(which)')
        return

    # Get index of data selected in eleana.dataset
    current_position = comboboxes.get_current_position(app, eleana, combobox_main)
    index_in_dataset = current_position['index_dataset']

    # Save current value in eleana.selections
    eleana.selections[which] = index_in_dataset

    # Create list of stack and save in eleana.combobox_lists
    eleana.combobox_lists[combobox_stk] = eleana.dataset[index_in_dataset].parameters['stk_names']
    comboboxes.populate_lists(app, eleana)

    # Update GUI buttons according to selections
    update.gui_widgets(app, eleana, comboboxes)

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
app = EleanaMainApp()
eleana = Eleana()
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
