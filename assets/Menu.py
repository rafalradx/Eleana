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
        self.borderwidth = 1

        # Icons
        self.icon_dropdown = self.prepare_icon("dropdown.png")
        self.icon_load_project = self.prepare_icon("load-project.png")
        self.icon_recent_projects = self.prepare_icon("recent_projects.png")
        self.icon_save_as = self.prepare_icon("save_as.png")
        self.icon_import = self.prepare_icon("import.png")
        self.icon_exit = self.prepare_icon("exit.png")
        self.icon_epr = self.prepare_icon("epr.png")
        self.icon_export = self.prepare_icon("export.png")
        self.icon_none = self.prepare_icon("x.png")
        self.icon_trash = self.prepare_icon("trash.png")
        self.icon_clear = self.prepare_icon("clear.png")
        self.icon_notes = self.prepare_icon("notes.png")
        self.icon_graphPrefs = self.prepare_icon("graph_pref.png")
        self.icon_table = self.prepare_icon("table.png")

        ''' Menu Bar'''
        self.main_menu = tk.Menu(self.app.mainwindow, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.app.mainwindow.config(menu=self.main_menu)

        # FILE
        self.menu_file = tk.Menu(self.main_menu, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.main_menu.add_cascade(label="File", menu=self.menu_file, image = self.icon_dropdown, compound="left")

        # - Load project
        self.menu_file.add_command(label="Load project", command=self.app.load_project, image = self.icon_load_project, compound="left", accelerator="Ctrl+O")

        # - Recent projects:
        self.menu_recent = tk.Menu(self.menu_file, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_file.add_cascade(label="Recent projects", menu=self.menu_recent, image = self.icon_recent_projects, compound="left")

        # - Save As
        self.menu_file.add_command(label="Save As", command=self.app.save_as, image = self.icon_save_as, compound="left")
        # - Save As
        self.menu_file.add_command(label="Save", command=self.app.save_as, image=self.icon_save_as, compound="left", accelerator="Ctrl+S")

        # - Import data
        self.menu_import = tk.Menu(self.menu_file, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_file.add_cascade(label="Import data", menu=self.menu_import, image = self.icon_import, compound="left")

        # ------------ Bruker Elexsys
        self.menu_import.add_command(label="Bruker Elexsys (DTA)", command=self.app.import_elexsys, image = self.icon_epr, compound="left")
        # ------------ Bruker EMX
        self.menu_import.add_command(label="Bruker ESP/EMX (spc)", command=self.app.import_EMX, image = self.icon_epr, compound="left")
        # ------------ Adani dat
        self.menu_import.add_command(label="Adani text (dat)", command = self.app.import_adani_dat, image = self.icon_epr, compound="left")

        # ------------ Magnettech
        self.menu_import.add_command(label="Magnettech older (spe)", command=self.app.import_magnettech1,
                                     image=self.icon_epr,
                                     compound="left")
        self.menu_import.add_command(label="Magnettech newer (spe)", command=self.app.import_magnettech2,
                                     image=self.icon_epr,
                                     compound="left")
        # ------------ Separator
        self.menu_import.add_separator()

        # ------------ Shimadzu SPC
        self.menu_import.add_command(label="Shimadzu UV/VIS (spc)", command=self.app.import_shimadzu_spc, image=self.icon_epr,
                                     compound="left")

        # ------------ Separator
        self.menu_import.add_separator()

        # ------------ ASCII Files
        self.menu_import.add_command(label="ASCII file", command=self.app.import_ascii, image=self.icon_epr, compound="left")
        # ------------ Excel
        self.menu_import.add_command(label="MS Excel/LibreOffice Calc", command = self.app.load_excel, image = self.icon_epr, compound='left')

        # - SEPARATOR -
        self.menu_file.add_separator()


        # Export
        self.menu_export = tk.Menu(self.menu_file, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                   activebackground=self.activebg, activeforeground=self.activefg,
                                   borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_file.add_cascade(label="Export", menu=self.menu_export, image=self.icon_export, compound="left")
        # - Export first
        self.menu_export.add_command(label="Export First", command=self.app.export_first, image=self.icon_exit,
                                   compound="left")
        # - Export group
        self.menu_export.add_command(label="Export Group", command=self.app.export_group, image=self.icon_exit,
                                   compound="left", accelerator="Ctrl+Q")


        # - SEPARATOR -
        self.menu_file.add_separator()


        # - Quit
        self.menu_file.add_command(label="Quit", command=self.app.close_application, image = self.icon_exit, compound="left", accelerator="Ctrl+Q")


        ''' Menu EDIT'''

        #  EDIT
        self.menu_edit = tk.Menu(self.main_menu, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                 activebackground=self.activebg, activeforeground=self.activefg,
                                 borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.main_menu.add_cascade(label="Edit", menu=self.menu_edit, image = self.icon_dropdown, compound="left")

        # - Create from table
        #self.menu_edit.add_command(label="Create data from table", command=self.app.create_from_table, image=self.icon_table, compound="left")

        # - Delete selected data
        self.menu_edit.add_command(label="Delete selected data", command=self.app.delete_selected_data, image = self.icon_trash, compound="left")

        # - Notes
        self.menu_edit.add_command(label="Notes", command=self.app.notes, image = self.icon_notes, compound="left")

        # - Clear
        self.menu_clear = tk.Menu(self.menu_edit, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                 activebackground=self.activebg, activeforeground=self.activefg,
                                 borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_edit.add_cascade(label="Clear", menu=self.menu_clear, image = self.icon_clear, compound="left")

        # -------- Clear dataset
        self.menu_clear.add_command(label="Dataset", command=self.app.clear_dataset)

        # -------- Clear result
        self.menu_clear.add_command(label="Result", command=self.app.clear_results)


        # - First
        self.menu_groups = tk.Menu(self.menu_edit, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                 activebackground=self.activebg, activeforeground=self.activefg,
                                 borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_edit.add_cascade(label="Groups", menu=self.menu_groups, image=self.icon_dropdown, compound="left")
        # -------- Assign First to group
        self.menu_groups.add_command(label="Assign First to group", command=self.app.first_to_group)
        # -------- Assign Second to group
        self.menu_groups.add_command(label="Assign Second to group", command=self.app.second_to_group)

        # - Graph Preferences
        self.menu_edit.add_command(label="Graph preferences", command = self.app.graph_preferences, image=self.icon_graphPrefs, compound="left")


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
        self.context_menu_first.add_command(label="Assign to group", command=self.app.first_to_group)
        self.context_menu_first.add_command(label="Convert stack to group", command=lambda: self.app.stack_to_group('first'))
        self.context_menu_first.add_command(label="Rename", command=lambda: self.app.rename_data('first'))
        self.context_menu_first.add_command(label="Edit comment", command=lambda: self.app.edit_comment('first'))
    def build_menu_second(self):
        '''This creates positions for SECOND context menu '''
        self.context_menu_second.add_command(label="Second 1")
        self.context_menu_second.add_command(label="Second 2")

    def build_menu_result(self):
        '''This creates positions for SECOND context menu '''
        self.context_menu_result.add_command(label="Rename", command=lambda: self.app.rename_data('result'))
        self.context_menu_result.add_command(label="Result 2")

    def show_context_menu_first(self, event):
        self.context_menu_first.tk_popup(event.x_root, event.y_root)


    def show_context_menu_second(self, event):
        self.context_menu_second.tk_popup(event.x_root, event.y_root)

    def show_context_menu_result(self, event):
        self.context_menu_result.tk_popup(event.x_root, event.y_root)
        print('Context menu')

