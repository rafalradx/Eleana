import json
from pathlib import Path
import tkinter as tk
import customtkinter as ctk
import numpy as np
import pickle
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
class Init:
    def __init__(self, app, eleana_instance):
        self.app = app
        self.eleana = eleana_instance

    def main_window(self):
        '''This method sets properties of the main window'''

        width = self.app.mainwindow.winfo_screenwidth()  # Get screen width
        height = self.app.mainwindow.winfo_screenheight()  # Get screen height
        self.app.mainwindow.geometry('800x800')
        #app.mainwindow.geometry(str(width) + 'x' + str(height) + "+0+0")  # Set geometry to max


        # Add icon to the top window bar form pixmaps folder
        top_window_icon = Path(self.eleana.paths['pixmaps'], "eleana_top_window.png")
        main_icon = tk.PhotoImage(file=top_window_icon)
        self.app.mainwindow.iconphoto(True, main_icon)
        self.app.mainwindow.title('Eleana')
        # Set color motive for GUI
        ctk.set_default_color_theme("dark-blue")

        # ---------------------- Set default values in GUI -------
        self.app.sel_group.configure(values=['All'])
        self.app.sel_group.set('All')
        self.app.sel_first.configure(values=['None'])
        self.app.sel_first.set('None')
        self.app.sel_second.configure(values=['None'])
        self.app.sel_second.set('None')
        self.app.sel_result.configure(values=['None', 'yes'])
        self.app.sel_result.set('None')

        self.app.mainwindow.protocol('WM_DELETE_WINDOW', self.app.close_application)


    def folders(self):
        '''This method creates standard Eleana folder in user directory.
            If the folder does not exist it will be created.'''

        home_dir = self.eleana.paths['home_dir']
        eleana_user_dir = Path(home_dir, '.EleanaPy' )
        if not eleana_user_dir.exists():
            try:
                eleana_user_dir.mkdir()
            except:
                return {"Error": True, 'desc': f"Cannot create working Eleana folder in your home directory."}

    def paths(self, update):
        try:
            filename = Path(self.eleana.paths['home_dir'], '.EleanaPy', 'paths.pic')

            # Read paths.pic
            file_to_read = open(filename, "rb")
            paths = pickle.load(file_to_read)
            self.eleana.paths = paths
            file_to_read.close()

            # Create last project list in the main menu
            last_projects = self.eleana.paths['last_projects']
            last_projects = [element for i, element in enumerate(last_projects) if i <= 10]

            # Write the list to eleana.paths
            self.eleana.paths['last_projects'] = last_projects

            # Perform update to place the item into menu
            update.last_projects_menu()
        except:
            pass

    def eleana_variables(self):
        self.eleana.selections = {'group': 'All',
                      'first': -1, 'second': -1, 'result': -1,
                      'f_cpl': 're', 's_cpl': 're', 'r_cpl': 're',
                      'f_stk': 0, 's_stk': 0, 'r_stk': 0,
                      'f_dsp': True, 's_dsp': True, 'r_dsp': True
                      }

        self.eleana.notes = {"content": "",
                 "tags": {"bold": [], "italic": [], "code": [], "normal size": [], "larger size": [],
                          "largest size": [],
                          "highlight": [], "highlight red": [], "highlight green": [], "highlight black": [],
                          "text white": [], "text grey": [], "text blue": [], "text green": [], "text red": []}}

        self.eleana.dataset = []
        self.eleana.results_dataset = []
        self.eleana.assignmentToGroups = {}
        self.eleana.groupsHierarchy = {}

    # def graph_canvas(self, app):
    #     fig = plt.Figure(figsize=(8, 4), dpi=100)
    #     ax = fig.add_subplot(111)
    #
    #     # Generowanie danych dla funkcji sinc(x)
    #     x = np.linspace(-10, 10, 400)
    #     y = np.sinc(x)
    #
    #     # Rysowanie wykresu funkcji sinc(x)
    #     ax.plot(x, y, color='b', linewidth=2)
    #
    #     graph_canvas = FigureCanvasTkAgg(fig, master=app.graphFrame)
    #     graph_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    #     graph_canvas.draw()
    #
    #     graph_toolbar = NavigationToolbar2Tk(graph_canvas, app.graphFrame, pack_toolbar=False)
    #     graph_toolbar.update()
    #     graph_toolbar.grid(row=1, column=0, sticky="ew")
    #     return graph_canvas