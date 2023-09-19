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
from assets.general_eleana_methods import Eleana
from assets.gui_actions.menu_actions import MenuAction
from assets.general_eleana_methods import Update
from assets.subprogs.dialog_quit import QuitDialog

# Create Eleana additional instances
eleana = Eleana()
menuAction = MenuAction()
update = Update()

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui" / "Eleana_main.ui"

class EleanaMainApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("Eleana", master)
        # Main menu
        _main_menu = builder.get_object("mainmenu", self.mainwindow)
        self.mainwindow.configure(menu=_main_menu)

        self.group_down = None
        self.group_up = None
        self.group = None
        self.first_down = None
        builder.import_variables(
            self, ['group_down', 'group_up', 'group', 'first_down'])

        builder.connect_callbacks(self)

        # Create references to Widgets
        self.sel_group = builder.get_object("sel_group", self.mainwindow)
        self.sel_first = builder.get_object("sel_first", self.mainwindow)
        self.sel_second = builder.get_object("sel_second", self.mainwindow)
        self.sel_result = builder.get_object("sel_result", self.mainwindow)
        self.firstframe = builder.get_object("firstFrame", self.mainwindow)


    def run(self):
        self.mainwindow.mainloop()

    def group_down_clicked(self):
        pass

    def group_up_clicked(self):
        pass

    def group_selected(self, value):
        pass

    def first_down_clicked(self):
        pass

    def first_up_clicked(self):
        pass

    def first_selected(self, value):
        selected_value_text = app.sel_first.get()
        numbered_names = []
        for each in eleana.dataset:
            numbered_names.append(each.name_nr)

        if selected_value_text in numbered_names:
            index = numbered_names.index(selected_value_text)

        else:
            pass
        eleana.selections['first'] = index
        data_for_plot = eleana.dataset[index].get('first')
        x = data_for_plot['x']
        y = data_for_plot['y']
        create_matplotlib_chart(x, y)

    def second_down_clicked(self):
        pass

    def second_up_clicked(self):
        pass

    def results_down_clicked(self):
        pass

    def results_up_clicked(self):
        pass

    # Functions triggered by Menu selections
    # FILE
    # --- Import EPR --> Bruker Elexsys
    def import_elexsys(self):
        menuAction.loadElexsys()

        # When selected group is 'All' or 'all' (case insensitive) then get names of whole dataset (func. update.dataset_list)
        if eleana.selections['group'] == 'All':
            update.dataset_list()
            entries = ['None']
            for each in eleana.dataset:
                entries.append(each.name_nr)
            print(entries)
        # When there is different group selected then take names from this group
        else:
            entries = update.data_in_group_list()
        # Update values in Comboboxes
        app.sel_first.configure(values=entries)
        app.sel_second.configure(values=entries)

        i = 0
        while i < len(eleana.dataset):
            eleana.dataset[i].name
            i += 1

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


# ----------------------- Start GUI  --------------------------------

app = EleanaMainApp()

# -----------------------Prepare references to elements -------------
# Set references to particular ID in the tkinter interface
# For example if there is element with id="mainFrame" then create app.menu_import using following command:
# app.mainFrame = app.builder.get_object('graphFrame', app.mainwindow)

app.graphFrame = app.builder.get_object('graphFrame', app.mainwindow)


# -----------------------Set geometry and icon ----------------------
width = app.mainwindow.winfo_screenwidth()  # Get screen width
height = app.mainwindow.winfo_screenheight()  # Get screen height
app.mainwindow.geometry(str(width) + 'x' + str(height) + "+0+0")  # Set geometry to max
# Add icon to the top window bar form pixmaps folder
top_window_icon = Path(eleana.paths['pixmaps'], "eleana_top_window.png")
main_icon = tk.PhotoImage(file=top_window_icon)
app.mainwindow.iconphoto(True, main_icon)
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

# -----------------------------------------------------------------------
# --------          DIFFERENT UNUSED COMMENTS               -------------
# ------------------------------------------------------------------------

# Przykład umieszczenia przycisku wewnątrz ramki graphFrame:
# etykieta = ctk.CTkLabel(app.graphFrame, text="tekst") # Utwórz przycisk "etykieta" przez customtkinter
# etykieta.grid(column=0, padx=2, pady=2, row=0) # Umieść w warstwie stosując metodę grid


# Set comboboxes
# def update_combobox_values(widget, new_values):
#
#    app.sel_first.configure(values=new_values)  # This is for CTkcombobox which is different than tkinter
#    print(app.sel_first['values'])
