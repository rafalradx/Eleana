import tkinter as tk
from pathlib import Path
from LoadSave import Save

class MainMenu:
    def __init__(self, app_instance):
        self.app = app_instance
        self.eleana = app_instance.eleana
        self.icons = self.eleana.paths['pixmaps']

        ''' Styling of the menu '''
        self.bg = '#303030'
        self.fg = '#aaaaaa'
        self.font = ("Arial", 10)
        self.activebg = "#676767" # Hover background
        self.activefg = "#eaeaea" # Hover font color
        self.borderwidth = 1
        self.borderwidth_bar = 0

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
        self.icon_clipboard = self.prepare_icon("clipboard.png")
        self.icon_shimadzu = self.prepare_icon("shimadzu.png")
        self.icon_import_ascii = self.prepare_icon("import_ascii.png")
        self.icon_import_excel = self.prepare_icon("import_excel.png")
        self.icon_import_elexsys = self.prepare_icon("import_elexsys.png")
        self.icon_import_emx = self.prepare_icon("import_emx.png")
        self.icon_import_adani = self.prepare_icon("import_adani.png")
        self.icon_edit_par = self.prepare_icon("edit_par.png")
        self.icon_integrate_region = self.prepare_icon("integrate_region.png")
        self.icon_statistics = self.prepare_icon("statistics.png")
        self.icon_create_static_plot = self.prepare_icon("create_static_plot.png")
        self.icon_delete_static_plot = self.prepare_icon("delete_static_plot.png")
        self.icon_export_first = self.prepare_icon("export_first.png")
        self.icon_export_group = self.prepare_icon("export_group.png")
        self.icon_normalize = self.prepare_icon("normalize.png")
        self.icon_distance = self.prepare_icon("distance.png")
        self.icon_static_plot = self.prepare_icon("static_plot.png")
        self.icon_graphtools = self.prepare_icon("graphtools.png")
        self.icon_clearrange = self.prepare_icon("clearrange.png")
        self.icon_trash = self.prepare_icon("trash.png")
        self.icon_trashres = self.prepare_icon("trash_res.png")
        self.icon_fromclipboard =self.prepare_icon("fromclipboard.png")
        self.icon_baselineplynom = self.prepare_icon("baseline.png")

        ''' BUILD MENU '''
        self.main_menu = tk.Menu(self.app.mainwindow, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth_bar, activeborderwidth=self.borderwidth)
        self.app.mainwindow.config(menu=self.main_menu)

        # FILE
        self.menu_file = tk.Menu(self.main_menu, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        #self.main_menu.add_cascade(label="File", menu=self.menu_file, image = self.icon_dropdown, compound="left")
        self.main_menu.add_cascade(label=" File ", menu=self.menu_file)

        # - Load project
        self.menu_file.add_command(label="Load project", command=self.app.load_project, image = self.icon_load_project, compound="left", accelerator="Ctrl+O")

        # - Recent projects:
        self.menu_recent = tk.Menu(self.menu_file, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_file.add_cascade(label="Recent projects", menu=self.menu_recent, image = self.icon_recent_projects, compound="left")

        # - Save As
        self.menu_file.add_command(label="Save As", command=self.app.save_as, image = self.icon_save_as, compound="left")
        # - Save
        self.menu_file.add_command(label="Save", command=self.app.save_current, image=self.icon_save_as, compound="left", accelerator="Ctrl+S")

        # - Import data
        self.menu_import = tk.Menu(self.menu_file, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_file.add_cascade(label="Import data", menu=self.menu_import, image = self.icon_import, compound="left")

        # ------------ Bruker Elexsys
        self.menu_import.add_command(label="Bruker Elexsys (DTA)", command=self.app.import_elexsys, image = self.icon_import_elexsys, compound="left")
        # ------------ Bruker EMX
        self.menu_import.add_command(label="Bruker ESP/EMX (spc)", command=self.app.import_EMX, image = self.icon_import_emx, compound="left")
        # ------------ Adani dat
        self.menu_import.add_command(label="Adani text (dat)", command = self.app.import_adani_dat, image = self.icon_import_adani, compound="left")

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
        self.menu_import.add_command(label="Shimadzu UV/VIS (spc)", command=self.app.import_shimadzu_spc, image=self.icon_shimadzu,
                                     compound="left")

        # ------------ Separator
        self.menu_import.add_separator()

        # ------------ ASCII Files
        self.menu_import.add_command(label="ASCII file", command=self.app.import_ascii, image=self.icon_import_ascii, compound="left")
        # ------------ Excel
        self.menu_import.add_command(label="MS Excel/LibreOffice Calc", command = self.app.load_excel, image = self.icon_import_excel, compound='left')

        # - SEPARATOR -
        self.menu_file.add_separator()

        # Export
        self.menu_export = tk.Menu(self.menu_file, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                   activebackground=self.activebg, activeforeground=self.activefg,
                                   borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_file.add_cascade(label="Export", menu=self.menu_export, image=self.icon_export, compound="left")
        # - Export first
        self.menu_export.add_command(label="Export First", command=self.app.export_first, image=self.icon_export_first,
                                   compound="left")
        # - Export group
        self.menu_export.add_command(label="Export Group", command=self.app.export_group, image=self.icon_export_group,
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
        #self.main_menu.add_cascade(label="Edit", menu=self.menu_edit, image = self.icon_dropdown, compound="left")
        self.main_menu.add_cascade(label=" Edit ", menu=self.menu_edit)

        self.menu_spreadsheet = tk.Menu(self.menu_edit, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                 activebackground=self.activebg, activeforeground=self.activefg,
                                 borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)

        self.menu_edit.add_cascade(label="Spreadsheet", menu=self.menu_spreadsheet, image=self.icon_dropdown, compound="left")

        # - Create from table
        self.menu_edit.add_command(label="Create data from table", command=self.app.create_from_table, image=self.icon_table, compound="left")

        # - Edit parameters
        self.menu_edit.add_command(label="Edit parameters", command = self.app.edit_parameters, image=self.icon_edit_par, compound="left")

        # - SEPARATOR -
        self.menu_edit.add_separator()

        # - Copy to clipboard
        self.menu_edit.add_command(label="Copy", command=self.app.quick_paste, image=self.icon_clipboard, compound="left", accelerator='Ctrl+C')
        # - Create from clipboard
        self.menu_edit.add_command(label="Paste", command=self.app.quick_paste,  image=self.icon_fromclipboard, compound="left", accelerator='Ctrl+V')

        # - SEPARATOR -
        self.menu_edit.add_separator()

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
        self.menu_clear.add_command(label="Dataset", image = self.icon_trash, command=self.app.clear_dataset, compound="left")

        # -------- Clear result
        self.menu_clear.add_command(label="Result", image = self.icon_trashres, command=self.app.clear_results, compound="left")

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
        self.menu_edit.add_command(label="Preferences", command = self.app.preferences, image=self.icon_graphPrefs, compound="left")

        ''' Menu ANALYSIS '''

        # ANALYSIS
        self.menu_analysis = tk.Menu(self.main_menu, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                            activebackground=self.activebg, activeforeground=self.activefg,
                            borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        #self.main_menu.add_cascade(label="Analysis", menu=self.menu_analysis, image=self.icon_dropdown, compound="left")
        self.main_menu.add_cascade(label=" Analysis ", menu=self.menu_analysis)

        #  - Distance read
        self.menu_analysis.add_command(label="Calculate XY Distance", command=self.app.xy_distance,
                                       image=self.icon_distance, compound="left")

        #  - Integrate region
        self.menu_analysis.add_command(label="Integrate region", command=self.app.integrate_region,
                                  image=self.icon_integrate_region, compound="left")
        #  - Statistics
        self.menu_analysis.add_command(label="Statistics", command=self.app.quick_paste,
                                   image=self.icon_statistics, compound="left")

        ''' Menu MODIFICATIONS '''
        self.menu_modifications = tk.Menu(self.main_menu, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                     activebackground=self.activebg, activeforeground=self.activefg,
                                     borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        #self.main_menu.add_cascade(label="Modifications", menu=self.menu_modifications, image=self.icon_dropdown, compound="left")
        self.main_menu.add_cascade(label=" Modifications ", menu=self.menu_modifications)

        # - Normalize amplitude
        self.menu_modifications.add_command(label="Normalize amplitude", command=self.app.normalize,
                                       image=self.icon_normalize, compound="left")

        self.menu_modifications.add_separator()

        self.menu_modifications.add_command(label="Polynomial baseline", command=self.app.polynomial_baseline,
                                            image=self.icon_baselineplynom, compound="left")




        ''' Menu EPR '''
        self.menu_EPR = tk.Menu(self.main_menu, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                          activebackground=self.activebg, activeforeground=self.activefg,
                                          borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        #self.main_menu.add_cascade(label="EPR", menu=self.menu_EPR, image=self.icon_dropdown, compound="left")
        self.main_menu.add_cascade(label="EPR ", menu=self.menu_EPR)

        ''' Menu Tools '''
        self.menu_tools = tk.Menu(self.main_menu, tearoff=1, bg=self.bg, fg=self.fg, font=self.font,
                                 activebackground=self.activebg, activeforeground=self.activefg,
                                 borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)


        self.main_menu.add_cascade(label="Tools", menu=self.menu_tools)
        self.menu_graphtools = tk.Menu(self.main_menu, tearoff=1, bg=self.bg, fg=self.fg, font=self.font,
                                  activebackground=self.activebg, activeforeground=self.activefg,
                                  borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)

        # - Graph tools
        self.menu_tools.add_cascade(label="Graph tools", menu=self.menu_graphtools, image=self.icon_graphtools, compound="left")

        # ---- Clear selected range
        self.menu_graphtools.add_command(label="Clear selected range", command=self.app.clear_selected_ranges,
                                    image=self.icon_clearrange, compound="left")



        # - Create plot
        self.menu_tools.add_command(label="Create plot", command=self.app.create_simple_static_plot,
                                    image=self.icon_create_static_plot, compound="left")

        # - Delete plot
        self.menu_tools.add_command(label="Delete plot", command=self.app.delete_simple_static_plot,
                                    image=self.icon_delete_static_plot, compound="left")

        # -Separator
        self.menu_tools.add_separator()

        # ---- ENTRIES IN menu_showPlots ARE GENERATED DYNAMICALLY

        ''' Menu HELP '''
        self.menu_help = tk.Menu(self.main_menu, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                activebackground=self.activebg, activeforeground=self.activefg,
                                borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        #self.main_menu.add_cascade(label="Help", menu=self.menu_help, image=self.icon_dropdown, compound="left")
        self.main_menu.add_cascade(label="Help", menu=self.menu_help)

        # - About
        self.menu_help.add_command(label="About", command=self.app.quick_paste,
                                       image=self.icon_statistics, compound="left")

    def prepare_icon(self, filename):
            ''' This method prepares icon photoimage that is named "filename" '''
            icon_file = Path(self.icons, filename)
            icon = tk.PhotoImage(file=icon_file)
            return icon

    def last_projects_menu(self):
        ''' Updates list of the recently loaded or saved projects and adds the list to the main menu'''
        def _clear_recent_list():
            last = self.eleana.paths['last_projects'][0]
            self.eleana.paths['last_projects'] = [last]
            self.last_projects_menu()
            Save.save_settings_paths(self.eleana)
        list_for_menu = []
        i = 1
        for each in self.eleana.paths['last_projects']:
            item = Path(each)
            item = str(i) + '. ' + item.name
            list_for_menu.append(item)
            i += 1
        recent_menu = self.menu_recent
        recent_menu.delete(0, tk.END)
        icon_file = Path(self.eleana.paths['pixmaps'], 'project.png')
        icon_clear = tk.PhotoImage(file=icon_file)
        for label in list_for_menu:
            def create_command(l):
                return lambda: self.app.load_recent(l)
            recent_menu.add_command(label=label, image=icon_clear, compound="left", command=create_command(label))
        # Separator and clear
        recent_menu.add_separator()
        recent_menu.add_command(label='Keep only last', image=icon_clear, compound="left", command=_clear_recent_list)

    def create_showplots_menu(self):
        '''
        Take list of created plots and add to self.menu_showPlots.
        Remove the self.menu_showPlots if the list in self.eleana.static_plots is empty
        '''

        # Remove the current submenu and check if there are plots in the self.eleana.static_plots
        # If not then return
        try:
            self.menu_tools.delete("Show plot")
        except:
            pass

        if not self.eleana.static_plots:
            return
        # Create new menu
        self.menu_showPlots = tk.Menu(self.menu_file, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                      activebackground=self.activebg, activeforeground=self.activefg,
                                      borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_tools.add_cascade(label="Show plot", menu=self.menu_showPlots, image=self.icon_dropdown,
                                    compound="left")
        # Scan the content of self.eleana.static_plots to populate menu items
        i = 0
        while i < len(self.eleana.static_plots):
            # Replace forbidden marks
            name = self.eleana.static_plots[i]['name']
            name = name.replace('.', '-')
            name = name.replace(',', '-')
            name = name.replace('/', '-')
            name = name.replace(':', '-')
            self.eleana.static_plots[i]['name'] = name
            new_name_nr = str(i + 1) + '. ' + name
            self.eleana.static_plots[i]['name_nr'] = new_name_nr
            self.menu_showPlots.add_command(label=new_name_nr, command=lambda position=i: self.app.grapher.show_static_graph_window(position),
                                       image=self.icon_static_plot, compound="left")
            i += 1

class ContextMenu:
    ''' Create shortcut menu triggered by right mouse button'''
    def __init__(self, app_instance):
        self.app = app_instance
        self.eleana = app_instance.eleana

        ''' Styling of the context menu '''
        self.bg = '#505050'
        self.fg = '#aaaaaa'
        self.font = ("Arial", 10)

        ''' References to Widgets '''
        # GROUPS
        self.app.groupFrame.bind("<Button-3>", self.show_context_menu_group)
        self.app.sel_group.bind("<Button-3>", self.show_context_menu_group)
        self.context_menu_group = tk.Menu(self.app.mainwindow, tearoff=0, bg=self.bg, fg=self.fg, font=self.font)

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
        self.build_menu_group()
        self.build_menu_first()
        self.build_menu_second()
        self.build_menu_result()

    def build_menu_group(self):
        '''This creates positions for FIRST context menu '''
        self.context_menu_group.add_command(label="Remove assignments to the group", command=self.app.delete_group)
        self.context_menu_group.add_command(label="Assign data to additional group", command=lambda: self.app.data_to_other_group(move=False))
        self.context_menu_group.add_command(label="Move data to other group", command=lambda: self.app.data_to_other_group(move=True))
        self.context_menu_group.add_command(label="Delete data assigned to the group",  command=self.app.delete_data_from_group)
        self.context_menu_group.add_command(label ="Convert whole group to a stack", command=lambda: self.app.convert_group_to_stack(all = True))
        self.context_menu_group.add_command(label="Convert selected to a stack", command=lambda: self.app.convert_group_to_stack(all=False))

    def build_menu_first(self):
        '''This creates positions for FIRST context menu '''
        self.context_menu_first.add_command(label="Rename", command=lambda: self.app.rename_data('first'))
        self.context_menu_first.add_command(label="Delete", command=lambda: self.app.delete_data('first'))
        self.context_menu_first.add_command(label="Duplicate", command=lambda: self.app.duplicate_data('first'))
        self.context_menu_first.add_command(label="Assign to group", command=self.app.first_to_group)
        self.context_menu_first.add_command(label="Convert stack to group", command=lambda: self.app.stack_to_group('first'))
        self.context_menu_first.add_command(label="Edit comment", command=lambda: self.app.edit_comment('first'))
        self.context_menu_first.add_command(label="Edit parameters", command = lambda: self.app.edit_parameters('first'))

    def build_menu_second(self):
        '''This creates positions for SECOND context menu '''
        self.context_menu_second.add_command(label="Rename", command=lambda: self.app.rename_data('second'))
        self.context_menu_second.add_command(label="Delete", command=lambda: self.app.delete_data('second'))
        self.context_menu_second.add_command(label="Duplicate", command=lambda: self.app.duplicate_data('second'))
        self.context_menu_second.add_command(label="Assign to group", command=self.app.second_to_group)
        self.context_menu_second.add_command(label="Convert stack to group", command=lambda: self.app.stack_to_group('second'))
        self.context_menu_second.add_command(label="Edit comment", command=lambda: self.app.edit_comment('second'))
        self.context_menu_second.add_command(label="Edit parameters", command=lambda: self.app.edit_parameters('second'))

    def build_menu_result(self):
        '''This creates positions for SECOND context menu '''
        self.context_menu_result.add_command(label="Rename", command=lambda: self.app.rename_data('result'))
        self.context_menu_result.add_command(label="Delete", command=lambda: self.app.delete_data('result'))
        self.context_menu_second.add_command(label="Duplicate", command=lambda: self.app.duplicate_data('result'))

    def show_context_menu_group(self, event):
        self.context_menu_group.tk_popup(event.x_root, event.y_root)
    def show_context_menu_first(self, event):
        self.context_menu_first.tk_popup(event.x_root, event.y_root)

    def show_context_menu_second(self, event):
        self.context_menu_second.tk_popup(event.x_root, event.y_root)

    def show_context_menu_result(self, event):
        self.context_menu_result.tk_popup(event.x_root, event.y_root)
        print('Context menu')
