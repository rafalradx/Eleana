import tkinter as tk
from tkinter import ttk
import pathlib
from pathlib import Path

class MainMenu:
    def __init__(self, app_instance, eleana_instance):
        self.app = app_instance
        self.eleana = eleana_instance
        self.icons = self.eleana.paths['pixmaps']

        ''' Styling of the menu '''
        self.bg = '#303030'
        self.fg = '#aaaaaa'
        self.font = ("Arial", 10)
        self.activebg = "#676767" # Hover background
        self.activefg = "#eaeaea" # Hover font color
        self.borderwidth = 0

        # Icons
        self.icon_dropdown = self.prepare_icon("dropdown.png")
        self.icon_load_project = self.prepare_icon("load-project.png")
        self.icon_recent_projects = self.prepare_icon("recent_projects.png")
        self.icon_save_as = self.prepare_icon("save_as.png")
        self.icon_import = self.prepare_icon("import.png")
        self.icon_exit = self.prepare_icon("exit.png")
        self.icon_epr = self.prepare_icon("epr.png")

        ''' Menu Bar'''
        self.main_menu = tk.Menu(self.app.mainwindow, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.app.mainwindow.config(menu=self.main_menu)

        # FILE
        self.menu_file = tk.Menu(self.main_menu, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.main_menu.add_cascade(label="File", menu=self.menu_file, image = self.icon_dropdown, compound="left")

        # - Load project
        self.menu_file.add_command(label="Load project", command=self.app.load_project, image = self.icon_load_project, compound="left")

        # - Recent projects:
        self.menu_recent = tk.Menu(self.menu_file, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_file.add_cascade(label="Recent projects", menu=self.menu_recent, image = self.icon_recent_projects, compound="left")

        # - Save As
        self.menu_file.add_command(label="Save As", command=self.app.save_as, image = self.icon_save_as, compound="left")

        # - Import data
        self.menu_import = tk.Menu(self.menu_file, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_file.add_cascade(label="Import data", menu=self.menu_import, image = self.icon_import, compound="left")

        # ------------ Bruker Elexsys
        self.menu_import.add_command(label="Bruker Elexsys", command=self.app.import_elexsys, image = self.icon_epr, compound="left")
        # ------------ Bruker EMX
        self.menu_import.add_command(label="Bruker EMX", command=self.app.import_elexsys, image = self.icon_epr, compound="left")

        # - SEPARATOR -
        self.menu_file.add_separator()

        # - Quit
        self.menu_file.add_command(label="Quit", command=self.app.close_application, image = self.icon_exit, compound="left")

        #  EDIT
        self.menu_edit = tk.Menu(self.main_menu, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                 activebackground=self.activebg, activeforeground=self.activefg,
                                 borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.main_menu.add_cascade(label="Edit", menu=self.menu_edit, image = self.icon_dropdown, compound="left")

        # - Notes
        self.menu_edit.add_command(label="Notes", command=self.app.notes)

        # - Clear
        self.menu_clear = tk.Menu(self.menu_edit, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                 activebackground=self.activebg, activeforeground=self.activefg,
                                 borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_edit.add_cascade(label="Clear", menu=self.menu_clear)

        # -------- Clear dataset
        self.menu_clear.add_command(label="Dataset", command=self.app.clear_dataset)

        # -------- Clear result
        self.menu_clear.add_command(label="Result", command=self.app.clear_results)

    def prepare_icon(self, filename):
        ''' This method prepares icon photoimage that is named "filename" '''
        icon_file = Path(self.icons, filename)
        icon = tk.PhotoImage(file=icon_file)
        return icon

class ContextMenu:
    def __init__(self, app_instance, eleana_instance):
        self.app = app_instance
        self.eleana = eleana_instance

        ''' Styling of the context menu '''
        self.bg = '#505050'
        self.fg = '#aaaaaa'
        self.font = ("Arial", 10)

        ''' References to Widgets '''
        # FIRST
        self.app.firstFrame.bind("<Button-3>", self.show_context_menu_first)
        self.app.sel_first.bind("<Button-3>", self.show_context_menu_first)
        self.context_menu_first = tk.Menu(self.app.mainwindow, tearoff=0, bg=self.bg, fg=self.fg, font = self.font)

        # SECOND
        self.app.secondFrame.bind("<Button-3>", self.show_context_menu_second)
        self.app.sel_second.bind("<Button-3>", self.show_context_menu_second)
        self.context_menu_second = tk.Menu(self.app.mainwindow, tearoff=0, bg=self.bg, fg=self.fg, font = self.font)
        # RESULT
        self.app.resultFrame.bind("<Button-3>", self.show_context_menu_result)
        self.app.sel_result.bind("<Button-3>", self.show_context_menu_result)
        self.context_menu_result = tk.Menu(self.app.mainwindow, tearoff=0, bg=self.bg, fg=self.fg, font = self.font)

        # Build context menu for FIRST
        self.build_menu_first()
        self.build_menu_second()
        self.build_menu_result()
    def build_menu_first(self):
        '''This creates positions for FIRST context menu '''
        self.context_menu_first.add_command(label="First 1", command=self.app.context_first_pos1)
        self.context_menu_first.add_command(label="First 2", command=self.app.context_first_pos2)

    def build_menu_second(self):
        '''This creates positions for SECOND context menu '''
        self.context_menu_second.add_command(label="Second 1")
        self.context_menu_second.add_command(label="Second 2")

    def build_menu_result(self):
        '''This creates positions for SECOND context menu '''
        self.context_menu_result.add_command(label="Result 1")
        self.context_menu_result.add_command(label="Result 2")

    def show_context_menu_first(self, event):
        self.context_menu_first.tk_popup(event.x_root, event.y_root)


    def show_context_menu_second(self, event):
        self.context_menu_second.tk_popup(event.x_root, event.y_root)

    def show_context_menu_result(self, event):
        self.context_menu_result.tk_popup(event.x_root, event.y_root)
        print('Context menu')

