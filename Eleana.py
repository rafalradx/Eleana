#!/usr/bin/python3

# Import Standard Python Modules
import pathlib
import subprocess
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import customtkinter as ctk
import pygubu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
from json import loads, dumps

# Import Eleana specific classes
from assets.general_eleana_methods import Eleana, Update, ComboboxLists
from assets.gui_actions.menu_actions import MenuAction
from assets.subprogs.dialog_quit import QuitDialog

# Create main Eleana instances
eleana = Eleana()
menuAction = MenuAction()
update = Update()
comboboxLists = ComboboxLists()

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
            return
            # Get index of data selected in first in eleana.dataset
        current_position = comboboxLists.current_position(app, 'sel_first')
        index = int(current_position['index']) -1
        eleana.selections['first'] = index
            # Update GUI buttons according to selections
        update.selections_widgets(app)

        # Get data for plotting
        data_for_plot = eleana.getDataFromSelection('first')



            # Here will be fuction that generates graph
        x = data_for_plot['x']
        y = data_for_plot['re_y']
        create_matplotlib_chart(x, y)

    def f_stk_selected(self):
        print("Value")

    def second_selected(self, selected_value_text):
        if selected_value_text == 'None':
            return
            # Get index of data selected in first in eleana.dataset
        current_position = comboboxLists.current_position(app, 'sel_second')
        index = int(current_position['index']) - 1
        eleana.selections['second'] = index
        # Update GUI buttons according to selections
        update.selections_widgets(app)

        # Get data for plotting
        data_for_plot = eleana.getDataFromSelection('second')

        data_for_plot = eleana.dataset[index].get
            # x = data_for_plot['x']
            # y = data_for_plot['y']
            # create_matplotlib_chart(x, y)


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

    def results_down_clicked(self):
        pass

    def results_up_clicked(self):
        pass

    # Functions triggered by Menu selections
    # FILE
    # --- Import EPR --> Bruker Elexsys

    def import_elexsys(self):
        ''' Open window that loads the spectra '''
        menuAction.loadElexsys()

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
            update.dataset_list()
            comboboxLists.create_all_lists(app)

    # --- Quit (also window close by clicking on X)
    def close_application(self):
        # Display dialog window created in dialog_quit.py
        def quit_button_clicked():
            # This closes the pop-up window and then main application
            dialog_quit.window.destroy()
            app.mainwindow.destroy()

        # Create instance of the dialog window
        dialog_quit = QuitDialog(master=app.mainwindow)
        # Define function called after clicking quit_button
        dialog_quit.btn_quit.configure(command=quit_button_clicked)
    # EDIT Menu:
    #   Notes
    def notes(self):
        filename=menuAction.notes()
        print(filename)
        # Grab result

        file_back = eleana.read_tmp_file(filename)
        Eleana.notes = json.loads(file_back)




'''Initialization of the App and GUI'''

app = EleanaMainApp()

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
update.selections_widgets(app)




# ----------- Examples and tests ------------------------

# Umieszczenie matplotlib wykresu w app.graphframe
def create_matplotlib_chart(x,y):
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    #x = [1, 2, 3, 4, 5]
    #y = [10, 8, 6, 4, 2]

    ax.plot(x, y, label="Przykładowe dane")
    ax.set_xlabel('Oś x')
    ax.set_ylabel('Os y')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=app.graphFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")



x = [1, 2, 3, 4, 5]
y = [10, 8, 6, 4, 2]


create_matplotlib_chart(x,y)
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
