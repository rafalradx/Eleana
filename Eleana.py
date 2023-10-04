#!/usr/bin/python3

# Import Standard Python Modules
import pathlib

import tkinter as tk

from pathlib import Path
import customtkinter as ctk
import numpy as np
import pygubu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from CTkMessagebox import CTkMessagebox
import json
from json import loads, dumps

# Import Eleana specific classes
from assets.general_eleana_methods import Eleana, Update, ComboboxLists
from assets.gui_actions.menu_actions import MenuAction
from assets.subprogs.dialog_quit import QuitDialog


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
        self.firstStkFrame =  builder.get_object("firstStkFrame", self.mainwindow)
        self.secondStkFrame = builder.get_object("secondStkFrame", self.mainwindow)
        self.firstComplex = builder.get_object("firstComplex", self.mainwindow)
        self.secondImaginary = builder.get_object("secondImaginary", self.mainwindow)
        self.resultImaginary = builder.get_object("resultImaginary", self.mainwindow)
        self.graphFrame = builder.get_object('graphFrame', self.mainwindow)
        self.f_stk = builder.get_object('f_stk', self.mainwindow)
        self.s_stk = builder.get_object('s_stk', self.mainwindow)
        self.r_stk = builder.get_object('s_stk', self.mainwindow)
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

    def first_selected(self, selected_value_text: str):
        if selected_value_text == 'None':
            show_plots()
            update.selections_widgets(app, eleana)
            return

        # Get index of data selected in first in eleana.dataset
        current_position = comboboxLists.current_position(app, 'sel_first')
        index = int(current_position['index']) -1
        eleana.selections['first'] = index

        # Update GUI buttons according to selections
        update.selections_widgets(app, eleana)

        # Plot graph
        show_plots()

    def f_stk_selected(self, selected_value_text):
        current_f_stk = comboboxLists.current_position(app, 'f_stk')
        current_sel_first = comboboxLists.current_position(app, 'sel_first')
        eleana.selections['f_stk'] = current_f_stk['index']
        self.first_selected(current_sel_first['current'])


    def second_selected(self, selected_value_text):
        if selected_value_text == 'None':
            update.selections_widgets(app, eleana)
            show_plots()
            return
        # Get index of data selected in first in eleana.dataset
        current_position = comboboxLists.current_position(app, 'sel_second')
        index = int(current_position['index']) - 1
        eleana.selections['second'] = index
        # Update GUI buttons according to selections
        update.selections_widgets(app, eleana)

        # Draw plot
        show_plots()


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
        comboboxLists.create_all_lists(app,eleana)

    # --- Save as
    def save_as(self):
        menuAction.save_as(eleana)


    # --- Import EPR --> Bruker Elexsys

    def import_elexsys(self):
        ''' Open window that loads the spectra '''
        menuAction.loadElexsys()
        update.dataset_list(eleana)
        comboboxLists.create_all_lists(app,eleana)

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
        filename=menuAction.notes()
        #print(filename)
        # Grab result

        file_back = eleana.read_tmp_file(filename)
        eleana.notes = json.loads(file_back)




'''Initialization of the App and GUI'''

app = EleanaMainApp()
eleana = Eleana()
menuAction = MenuAction()
update = Update()
comboboxLists = ComboboxLists()

# -----------------------Set geometry and icon ----------------------
width = app.mainwindow.winfo_screenwidth()  # Get screen width
height = app.mainwindow.winfo_screenheight()  # Get screen height
#app.mainwindow.geometry(str(width) + 'x' + str(height) + "+0+0")  # Set geometry to max
app.mainwindow.geometry('800x800')

# Add icon to the top window bar form pixmaps folder
top_window_icon = Path(eleana.paths['pixmaps'], "eleana_top_window.png")
main_icon = tk.PhotoImage(file=top_window_icon)
app.mainwindow.iconphoto(True, main_icon)
app.mainwindow.title('Eleana')
# Set color motive for GUI
ctk.set_default_color_theme("dark-blue")

# ---------------------- Set default values in GUI -------
app.sel_group.configure(values=['All'])
app.sel_group.set('All')
app.sel_first.configure(values=['None'])
app.sel_first.set('None')
app.sel_second.configure(values=['None'])
app.sel_second.set('None')
app.sel_result.configure(values=['None', 'yes'])
app.sel_result.set('None')

# Hide widgets at application start
update.selections_widgets(app, eleana)

# ----------- Examples and tests ------------------------

# Umieszczenie matplotlib wykresu w app.graphframe

def show_plots():
    '''Ta funkcja zbiera informacje o wszystkich wyborach i wyswietla odpowiednie
    wartości na wykresie.
    Funkcje trzeba rozbudowac o elementy, które sprawdzają czy mamy wyświetlić
    część także część urojoną. Wtedy do wykresu dokładamy po jednej krzywej, np. przerywanej
    do każdego wybor FIRST, SECOND itd.

    Ostatecznie funkcja zostanie przeniesiona do innego pliku
    '''
    fig = Figure(figsize=(5,4), dpi = 100)
    ax = fig.add_subplot(111)

    # FIRST
    index = comboboxLists.current_position(app, 'sel_first')['index']
    if index != 0:
        is_first_not_none = True
    else:
        is_first_not_none = False

    if eleana.selections['f_dsp'] and is_first_not_none:
        data_for_plot = eleana.getDataFromSelection(eleana, 'first')
        data_index = eleana.selections['first']
        first_x = data_for_plot['x']
        first_re_y = data_for_plot['re_y']
        first_im_y = data_for_plot['im_y']
        first_legend_index = eleana.selections['first']
        first_legend = eleana.dataset[first_legend_index].name

        # Label for x axis
        try:
            label_x_title = eleana.dataset[data_index].parameters['name_x']
        except:
            label_x_title = ''
        try:
            label_x_unit = eleana.dataset[data_index].parameters['unit_x']
        except:
            label_x_unit = 'a.u.'
        first_label_x = label_x_title + ' [' + label_x_unit + ']'

        # Labels for y axis
        try:
            label_y_title = eleana.dataset[data_index].parameters['name_y']
        except:
            label_y_title = ''
        try:
            label_y_unit = eleana.dataset[data_index].parameters['unit_y']
        except:
            label_y_unit = 'a.u.'
        first_label_y = label_y_title + ' [' + label_y_unit + ']'

    else:
        first_x = np.array([])
        first_re_y = np.array([])
        first_im_y = np.array([])
        first_legend = 'no plot'
        first_label_x = ''
        first_label_y = ''

    # Add FIRST to plot
    ax.set_ylabel(first_label_y)
    ax.set_xlabel(first_label_x)
    ax.plot(first_x, first_re_y, label=first_legend)

    # SECOND
    index = comboboxLists.current_position(app, 'sel_second')['index']
    if index != 0:
        is_second_not_none = True
    else:
        is_second_not_none = False

    if eleana.selections['s_dsp'] and is_second_not_none:
        data_for_plot = eleana.getDataFromSelection(eleana, 'second')
        data_index = eleana.selections['second']
        second_x = data_for_plot['x']
        second_re_y = data_for_plot['re_y']
        second_im_y = data_for_plot['im_y']
        second_legend_index = eleana.selections['second']
        second_legend = eleana.dataset[second_legend_index].name

        # Label for x axis
        try:
            label_x_title = eleana.dataset[data_index].parameters['name_x']
        except:
            label_x_title = ''
        try:
            label_x_unit = eleana.dataset[data_index].parameters['unit_x']
        except:
            label_x_unit = 'a.u.'
        second_label_x = label_x_title + ' [' + label_x_unit + ']'

        # Labels for y axis
        try:
            label_y_title = eleana.dataset[data_index].parameters['name_y']
        except:
            label_y_title = ''
        try:
            label_y_unit = eleana.dataset[data_index].parameters['unit_y']
        except:
            label_y_unit = 'a.u.'
        second_label_y = label_y_title + ' [' + label_y_unit + ']'

    else:
        second_x = np.array([])
        second_re_y = np.array([])
        second_im_y = np.array([])
        second_legend = 'no plot'
        second_label_x = ''
        second_label_y = ''

    # Add SECOND to plot
    if eleana.selections['f_dsp'] and is_first_not_none:
        # If FIRST spectrum is on then do not change axes labels
        pass
    else:
        # If FIRST spectrum is off or set tu None then change labels to those from SECOND
        ax.set_ylabel(second_label_y)
        ax.set_xlabel(second_label_x)

    ax.plot(second_x, second_re_y, label=second_legend)

    # RESULT
    if len(eleana.results_dataset) != 0:
        index = comboboxLists.current_position(app, 'sel_result')['index']
        if index != 0:
            is_result_not_none = True
        else:
            is_result_not_none = False

        if eleana.selections['s_dsp'] and is_result_not_none:
            data_for_plot = eleana.getDataFromSelection(eleana, 'result')
            data_index = eleana.selections['result']
            result_x = data_for_plot['x']
            result_re_y = data_for_plot['re_y']
            result_im_y = data_for_plot['im_y']
            result_legend_index = eleana.selections['result']
            result_legend = eleana.results_dataset[result_legend_index].name

            # Label for x axis
            try:
                label_x_title = eleana.results_dataset[data_index].parameters['name_x']
            except:
                label_x_title = ''
            try:
                label_x_unit = eleana.results_dataset[data_index].parameters['unit_x']
            except:
                label_x_unit = 'a.u.'
            result_label_x = label_x_title + ' [' + label_x_unit + ']'

            # Labels for y axis
            try:
                label_y_title = eleana.results_dataset[data_index].parameters['name_y']
            except:
                label_y_title = ''
            try:
                label_y_unit = eleana.results_dataset[data_index].parameters['unit_y']
            except:
                label_y_unit = 'a.u.'
            result_label_y = label_y_title + ' [' + label_y_unit + ']'

        else:
            result_x = np.array([])
            result_re_y = np.array([])
            result_im_y = np.array([])
            result_legend = 'no plot'
            result_label_x = ''
            result_label_y = ''

        # Add SECOND to plot
        if eleana.selections['f_dsp'] and eleana.selections['s_dsp'] and is_first_not_none and is_second_not_none:
            pass
        else:
            # If FIRST spectrum is off or set tu None then change labels to those from SECOND
            ax.set_ylabel(result_label_y)
            ax.set_xlabel(result_label_x)

        ax.plot(result_x, result_re_y, label=result_legend)

    # Put data on Graph
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=app.graphFrame)
    canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    canvas.draw()
    app.graphFrame.columnconfigure(0, weight=1)
    app.graphFrame.rowconfigure(0, weight=1)


# Sposób na ukrycie
#app.sel_first.grid_remove()
#app.sel_first.grid(row=1, column=0, columnspan=3)

# ----------------- Final configuration and App Start---------------------
# Configure closing action
app.mainwindow.protocol('WM_DELETE_WINDOW', app.close_application)

# Run
if __name__ == "__main__":

    app.run()
