import json
from pathlib import Path
import tkinter as tk
import customtkinter as ctk
from json import loads, dumps
import pickle

class Init:

    def __init__(self, app, eleana_instance):
        self.app = app
        self.eleana = eleana_instance

    def main_window(self, app, eleana):
        '''This method sets properties of the main window'''

        width = self.app.mainwindow.winfo_screenwidth()  # Get screen width
        height = self.app.mainwindow.winfo_screenheight()  # Get screen height
        app.mainwindow.geometry('800x800')
        #app.mainwindow.geometry(str(width) + 'x' + str(height) + "+0+0")  # Set geometry to max


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

        app.mainwindow.protocol('WM_DELETE_WINDOW', app.close_application)


    def folders(self, app, eleana):
        '''This method creates standard Eleana folder in user directory.
            If the folder does not exist it will be created.'''

        home_dir = self.eleana.paths['home_dir']
        eleana_user_dir = Path(home_dir, '.EleanaPy' )
        if not eleana_user_dir.exists():
            try:
                eleana_user_dir.mkdir()
            except:
                return {"Error": True, 'desc': f"Cannot create working Eleana folder in your home directory."}

    def paths(self, app, eleana, update):
        try:
            filename = Path(eleana.paths['home_dir'], '.EleanaPy', 'paths.pic')

            # Read paths.pic
            file_to_read = open(filename, "rb")
            paths = pickle.load(file_to_read)
            eleana.paths = paths
            file_to_read.close()

            # Create last project list in the main menu
            last_projects = eleana.paths['last_projects']
            last_projects = [element for i, element in enumerate(last_projects) if i <= 10]

            # Write the list to eleana.paths
            eleana.paths['last_projects'] = last_projects

            # Perform update to place the item into menu
            update.last_projects_menu(app, eleana)
        except:
            pass

    def eleana_variables(self, eleana):
        eleana.selections = {'group': 'All',
                      'first': -1, 'second': -1, 'result': -1,
                      'f_cpl': 're', 's_cpl': 're', 'r_cpl': 're',
                      'f_stk': 0, 's_stk': 0, 'r_stk': 0,
                      'f_dsp': True, 's_dsp': True, 'r_dsp': True
                      }

        eleana.notes = {"content": "",
                 "tags": {"bold": [], "italic": [], "code": [], "normal size": [], "larger size": [],
                          "largest size": [],
                          "highlight": [], "highlight red": [], "highlight green": [], "highlight black": [],
                          "text white": [], "text grey": [], "text blue": [], "text green": [], "text red": []}}

        eleana.dataset = []
        eleana.results_dataset = []
        eleana.assignmentToGroups = {}
        eleana.groupsHierarchy = {}