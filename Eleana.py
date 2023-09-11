#!/usr/bin/python3

# Hello I am Dashboard
# OK. dodaje nową klasę przed class Eleana

# Import Standard Python Modules
import json
import pathlib
import subprocess
import tkinter as tk
from pathlib import Path
import customtkinter as ctk
import pygubu
from customtkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Import Eleana specific classes
from subprogs.general_eleana_methods import Eleana


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui" / "Eleana_main.ui"



class ale_to_jest_git():
    print("no nie wiem, chyba nie.")

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

        self.group = None
        self.group_down = None
        self.group_up = None
        self.first_down = None
        builder.import_variables(
            self, ['group', 'group_down', 'group_up', 'first_down'])

        builder.connect_callbacks(self)

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
        pass

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
    # -- Import EPR --> Bruker Elexsys
    def import_elexsys(self):
        MenuAction.import_elexsys(self)

    # --- Quit
    def quit(self):
        quit_application()

    # EDIT Menu:
    #   Notes
    def notes(self):
        subprocess_path = Path(Eleana.paths['subprogs'], 'editor.py')
        # Example of text for editor
        # content_to_sent = {"content": "Jaki\u015b przykladowy plik\n", "tags": {"bold": [], "italic": [], "code": [], "normal size": [], "larger size": [], "largest size": [], "highlight": [], "highlight red": [], "highlight green": [], "highlight black": [], "text white": [], "text grey": [], "text blue": [], "text green": [], "text red": []}}
        content_to_sent = Eleana.notes
        content_to_sent.update({'window_title': 'Edit notes'})  # Add text for window title

        filename = "eleana_edit_notes.rte"
        formatted_str = json.dumps(content_to_sent, indent=4)

        # Create /tmp/eleana_edit_notes.rte
        Eleana.create_tmp_file(self, filename, formatted_str)

        # Run editor in subprocess_path (./subprogs/edit.py) and wait for end
        notes = subprocess.run([Eleana.interpreter, subprocess_path], capture_output=True, text=True)

        # Grab result
        file_back = Eleana.read_tmp_file(self, filename)
        Eleana.notes = json.loads(file_back)


class UpdateCTkComboboxValues():
    def set_values(self, widget, val=['']):
        # This function sets the values to the combobox ascribed to widget. Widget can be "app.sel_first"
        widget.configure(values=val)

    def append_values(self, widget, val=['']):
        # This appends val[] to the widged combobox
        current = widget.cget('values')
        val = current + val
        widget.configure(values=val)

    def del_values(self, widget, between=(0, 0)):
        # This deletes the values between range in between[0] and between[1] from the widget combobx
        current = widget.cget('values')
        if between[0] > between[1]:
            between[0], between[1] = between[1], between[0]
        if between[0] < 0:
            between[0] = 0
        if between[1] > len(current) - 1:
            between[1] = len(current) - 1
        val = current[:between[0]] + current[between[1] + 1:]
        widget.configure(values=val)


# -----------------------FUNCTIONS -----------------------------------------

class MenuAction():
    def import_elexsys(self) -> object:
        filetypes = (
            ('Elexsys', '*.DSC'),
            ('All files', '*.*')
        )

        filenames = filedialog.askopenfilenames(initialdir=Eleana.paths['last_import_dir'], filetypes=filetypes)
        Eleana.load_elexsys(self, filenames)


    def quit(self):
        decission = subprocess.run(["python3", "libs/quit_dialog.py"], capture_output=True, text=True)
        print(decission.stdout[:4])
        if decission.stdout[:4] == "quit":
            app.mainwindow.destroy()


# -----------------------Prepare GUI  --------------------------------

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
top_window_icon = Path(Eleana.paths['pixmaps'], "eleana_top_window.png")
main_icon = tk.PhotoImage(file=top_window_icon)
app.mainwindow.iconphoto(True, main_icon)
# Set color motive for GUI
ctk.set_default_color_theme("dark-blue")


# -----------------------Set important variables ---------


def quit_application():
    subprocess_path = Path(Eleana.paths['subprogs'], 'quit_dialog.py')

    decission = subprocess.run(["python3.10", subprocess_path], capture_output=True, text=True)
    print(decission.stdout[:4])
    if decission.stdout[:4] == "quit":
        app.mainwindow.destroy()


# ----------- Examples and tests ------------------------

# Umieszczenie matplotlib wykresu w app.graphframe
def create_matplotlib_chart():
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    x = [1, 2, 3, 4, 5]
    y = [10, 8, 6, 4, 2]

    ax.plot(x, y, label="Przykładowe dane")
    ax.set_xlabel('Oś x')
    ax.set_ylabel('Os y')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=app.graphFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


create_matplotlib_chart()
app.graphFrame.columnconfigure(0, weight=1)
app.graphFrame.rowconfigure(0, weight=1)

# ----------------- Final configuration and App Start---------------------
# Configure closing action
app.mainwindow.protocol('WM_DELETE_WINDOW', quit_application)

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
