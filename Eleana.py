#!/usr/bin/python3

import json
# Import Standard Python Modules
import pathlib

import pygubu
from CTkMessagebox import CTkMessagebox

# Import Eleana specific classes
from assets.general_eleana_methods import Eleana, Update, ComboboxLists
from assets.gui_actions.menu_actions import MenuAction
from assets.initialization import Init
from assets.graph_plotter import plotter
# ------------------
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
        self.secondImaginary = builder.get_object("secondImaginary", self.mainwindow)
        self.resultImaginary = builder.get_object("resultImaginary", self.mainwindow)
        self.graphFrame = builder.get_object('graphFrame', self.mainwindow)
        self.f_stk = builder.get_object('f_stk', self.mainwindow)
        self.s_stk = builder.get_object('s_stk', self.mainwindow)
        self.r_stk = builder.get_object('s_stk', self.mainwindow)

        # Set default values
        self.firstComplex.set(value="re")

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
        current_entry_on_list = comboboxLists.current_position(app, 'sel_first')
        current_index_on_list = current_entry_on_list['index']
        if current_index_on_list == 0:
            return
        else:
            new_index_on_list = current_index_on_list - 1
            entries = comboboxLists.entries['sel_first']
            entry = entries[new_index_on_list]
            update.set_on_index(app, 'sel_first', entry)
            self.first_selected(entry)

    def first_up_clicked(self):
        current_entry_on_list = comboboxLists.current_position(app, 'sel_first')
        current_index_on_list = current_entry_on_list['index']
        last_index = current_entry_on_list['last_index']
        if current_index_on_list == last_index:
            return
        else:
            new_index_on_list = current_index_on_list + 1
            entries = comboboxLists.entries['sel_first']
            entry = entries[new_index_on_list]
            update.set_on_index(app, 'sel_first', entry)
            self.first_selected(entry)
        pass

    def first_complex_clicked(self, value):
        eleana.selections['f_cpl'] = value
        # current_position = comboboxLists.current_position(app, 'sel_first')
        # index = int(current_position['index']) - 1
        # eleana.selections['first'] = index

        # Update GUI buttons according to selections
        # update.selections_widgets(app, eleana)

        # Plot graph
        plotter(app, eleana, comboboxLists)

    def first_selected(self, selected_value_text: str):
        if selected_value_text == 'None':
            plotter(app, eleana, comboboxLists)
            update.selections_widgets(app, eleana)
            return

        # Get index of data selected in first in eleana.dataset
        current_position = comboboxLists.current_position(app, 'sel_first')
        index = int(current_position['index']) - 1
        eleana.selections['first'] = index

        # Update GUI buttons according to selections
        update.selections_widgets(app, eleana)

        # Plot graph
        plotter(app, eleana, comboboxLists)

    def f_stk_selected(self, selected_value_text):
        current_f_stk = comboboxLists.current_position(app, 'f_stk')
        current_sel_first = comboboxLists.current_position(app, 'sel_first')
        eleana.selections['f_stk'] = current_f_stk['index']
        self.first_selected(current_sel_first['current'])

    def second_selected(self, selected_value_text):
        if selected_value_text == 'None':
            update.selections_widgets(app, eleana)
            plotter(app, eleana, comboboxLists)
            return
        # Get index of data selected in first in eleana.dataset
        current_position = comboboxLists.current_position(app, 'sel_second')
        index = int(current_position['index']) - 1
        eleana.selections['second'] = index
        # Update GUI buttons according to selections
        update.selections_widgets(app, eleana)

        # Draw plot
        plotter(app, eleana, comboboxLists)

    def second_down_clicked(self):
        current_entry_on_list = comboboxLists.current_position(app, 'sel_second')
        current_index_on_list = current_entry_on_list['index']
        if current_index_on_list == 0:
            return
        else:
            new_index_on_list = current_index_on_list - 1
            entries = comboboxLists.entries['sel_second']
            entry = entries[new_index_on_list]
            update.set_on_index(app, 'sel_second', entry)
            self.second_selected(entry)
        pass

    def second_up_clicked(self):
        current_entry_on_list = comboboxLists.current_position(app, 'sel_second')
        current_index_on_list = current_entry_on_list['index']
        last_index = current_entry_on_list['last_index']
        if current_index_on_list == last_index:
            return
        else:
            new_index_on_list = current_index_on_list + 1
            entries = comboboxLists.entries['sel_second']
            entry = entries[new_index_on_list]
            update.set_on_index(app, 'sel_second', entry)
            self.second_selected(entry)
        pass

    def s_stk_selected(self, selected_value_text):
        current_s_stk = comboboxLists.current_position(app, 's_stk')
        current_sel_second = comboboxLists.current_position(app, 'sel_second')
        eleana.selections['s_stk'] = current_s_stk['index']
        self.second_selected(current_sel_second['current'])

    def results_down_clicked(self):
        pass

    def results_up_clicked(self):
        pass

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
        comboboxLists.create_all_lists(app, eleana)

    # --- Save as
    def save_as(self):
        menuAction.save_as(eleana)

    # --- Import EPR --> Bruker Elexsys

    def import_elexsys(self):
        ''' Open window that loads the spectra '''
        menuAction.loadElexsys()
        update.dataset_list(eleana)
        comboboxLists.create_all_lists(app, eleana)

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

        # Będę musiał dodać funkcję sprawdzenia grupy wewnątrz update.dataset_list
        if eleana.selections['group'] == 'All':
            update.dataset_list(eleana)
            comboboxLists.create_all_lists(app, eleana)

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


'''Create main instances 
app     - object of the main window containing GUI and tkinter and ctk widgets
eleana  - object containing base variables that store all information and dataset 
          that are available everywhere in the application.
menuAction - object containing methods to handle selections of items in the program menu
update  - object containing methods for refreshing GUI, creating lists in comboboxes etc
comboboxLists - methods for creating list, picking, setting items etc. They do not change GUI elements.
init    - object that is used to initialize program on start 
'''

app = EleanaMainApp()
eleana = Eleana()
menuAction = MenuAction()
update = Update()
comboboxLists = ComboboxLists()
init = Init()

# Set geometry, icon and default combobox values
init.main_window(app, eleana)
init.folders(eleana)


update.selections_widgets(app, eleana)

# Run
if __name__ == "__main__":
    app.run()
