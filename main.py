import sys

# BASIC CONFIGURATION
ELEANA_VERSION = 1              # Set the Eleana version. This will be stored in self.eleana.version
INTERPRETER = sys.executable    # Defines python version
DEVEL = True                    # For final product set to False - no errors will be displayed or print commands
                                # For development set to True. This is stored in self.eleana.devel_mode

# Import basic modules and add ./modules to sys.path
from pathlib import Path
import copy
import io
import re
import os
from functools import wraps
import customtkinter as ctk
import ctypes


# Set paths for assets, modules, subprogs and widgets
PROJECT_PATH = Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "Eleana_interface.ui"
MODULES = PROJECT_PATH / "modules"
ASSETS = PROJECT_PATH / "assets"
SUBPROGS = PROJECT_PATH / "subprogs"
WIDGETS = PROJECT_PATH / "widgets"
PIXMAPS = PROJECT_PATH / "pixmaps"

sys.path.insert(0, str(MODULES))
sys.path.insert(0, str(ASSETS))
sys.path.insert(0, str(SUBPROGS))
sys.path.insert(0,str(WIDGETS))

from assets.Eleana import Eleana
from assets.CommandProcessor import CommandProcessor

# Import External modules required
import numpy as np
import pandas

# Import modules from ./modules folder
import pygubu
from assets.Application import Application
from CTkListbox import CTkListbox
from CTkMessagebox import CTkMessagebox
from CTkScrollableDropdown import CTkScrollableDropdown
from widgets.CTkSpinbox import CTkSpinbox


# Import Eleana specific classes
# Widgets used by main application
from widgets.CTkHorizontalSlider import CTkHorizontalSlider

''' STARTING THE APPLICATION '''
#
# # Create general main instances for the program
# if not DEVEL:
#     # Switch off the error display in final product
#     if os.name == 'posix':  # Unix/Linux/macOS
#         sys.stderr = open(os.devnull, 'w')
#     elif os.name == 'nt':  # Windows
#         sys.stderr = open('nul', 'w')
#
#     # Switch off nupy RankWarnings in Numpy
#     import warnings
#     warnings.simplefilter('ignore', np.exceptions.RankWarning)



# Run
if __name__ == "__main__":
    # Check if the program is started with root privileges:
    if os.name == 'nt':
        # Windows
        try:
            disp_warn = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            disp_warn = False
    else:
        # Unix (Linux, macOS)
        disp_warn = os.geteuid() == 0

    # When root privileges detected, display warning
    if disp_warn:
        msg = CTkMessagebox(title="Warning!", message="For safety reasons, this program should not be run with administrator privileges.",
                            icon="warning", option_1="Quit", option_2="Ignore")
        if msg.get() == "Quit":
            sys.exit()

    if not DEVEL:
        # Switch off the error display in final product
        if os.name == 'posix':  # Unix/Linux/macOS
            sys.stderr = open(os.devnull, 'w')
        elif os.name == 'nt':  # Windows
            sys.stderr = open('nul', 'w')

        # Switch off nupy RankWarnings in Numpy
        import warnings

        warnings.simplefilter('ignore', np.exceptions.RankWarning)

    ''' Create Main instances '''
    eleana = Eleana(version=ELEANA_VERSION, devel=DEVEL)
    #sound = Sound()
    cmd = CommandProcessor()

    # Create application instance
    app = Application(eleana, cmd)  # This is GUI

    # Start application
    app.run()


    #
    # load = Load(main_menu)
    # save = Save(app)
    # export = Export(app)
    # init = Init(main_menu)
    # context_menu = ContextMenu(app)
    # update = Update(main_menu)  # This contains methods for update things like lists, settings, gui, groups etc.
    # app.set_update(update)
    #
    # # Initialize basic settings: geometry, icon, graph, binding, etc
    # init.main_window()
    # init.paths(update)
    # init.folders()
    # init.graph()

    # Command Line and tests

    # Create Graph canvas
    # grapher.plot_graph()
    # # Hide or show widgets in GUI
    # update.gui_widgets()
    # update.all_lists()
    #
    # # Set graph Frame scalable
    # app.graphFrame.columnconfigure(0, weight=1)
    # app.graphFrame.rowconfigure(0, weight=1)
    # main_menu.last_projects_menu()
    #
    #app.run()
