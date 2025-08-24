import tkinter as tk
from pathlib import Path
from LoadSave import Save

class MainMenu:
    def __init__(self, master, pixmap_folder, callbacks, eleana):
        self.icons = pixmap_folder
        self.callbacks = callbacks or {}
        self.master = master
        self.eleana = eleana

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
        self.icon_project2 = self.prepare_icon("project2.png")
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
        self.icon_splinebaseline = self.prepare_icon("spline.png")
        self.icon_trimdata = self.prepare_icon("trim.png")
        self.icon_btog = self.prepare_icon("Btog.png")
        self.icon_sav_gol = self.prepare_icon("sav_gol.png")
        self.icon_filter_general = self.prepare_icon('filter_general.png')
        self.icon_pseudomod = self.prepare_icon('pseudomod.png')
        self.icon_fftfilter = self.prepare_icon('fftfilter.png')
        self.icon_fft = self.prepare_icon('fft.png')
        self.icon_spectrasubtract = self.prepare_icon('subtract.png')

    def create(self, master):
        ''' BUILD MENU '''
        self.main_menu = tk.Menu(master, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth_bar, activeborderwidth=self.borderwidth)
        self.master.config(menu=self.main_menu)

        # FILE
        self.menu_file = tk.Menu(self.main_menu, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.main_menu.add_cascade(label="File ", menu=self.menu_file)

        # - Load project
        self.menu_file.add_command(label="Load project", command=self.callbacks.get("load_project"), image = self.icon_load_project, compound="left", accelerator="Ctrl+O")

        # - Recent projects:
        self.menu_recent = tk.Menu(self.menu_file, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_file.add_cascade(label="Recent projects", menu=self.menu_recent, image = self.icon_recent_projects, compound="left")

        # - Save As
        self.menu_file.add_command(label="Save As", command=self.callbacks.get("save_as"), image = self.icon_save_as, compound="left")

        # - Save
        self.menu_file.add_command(label="Save", command=self.callbacks.get("save_current"), image=self.icon_save_as, compound="left", accelerator="Ctrl+S")

        # # - Import data
        self.menu_import = tk.Menu(self.menu_file, tearoff=0, bg = self.bg, fg = self.fg, font = self.font, activebackground=self.activebg, activeforeground=self.activefg, borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_file.add_cascade(label="Import data", menu=self.menu_import, image = self.icon_import, compound="left")

        # ------------ Bruker Elexsys
        self.menu_import.add_command(label="Bruker Elexsys (DTA)", command=self.callbacks.get("import_elexsys"), image = self.icon_import_elexsys, compound="left")
        # ------------ Bruker EMX
        self.menu_import.add_command(label="Bruker ESP/EMX (spc)", command=self.callbacks.get("import_EMX"), image = self.icon_import_emx, compound="left")
        # ------------ Adani dat
        self.menu_import.add_command(label="Adani text (dat)", command = self.callbacks.get("import_adani_dat"), image = self.icon_import_adani, compound="left")

        # ------------ Magnettech
        self.menu_import.add_command(label="Magnettech older (spe)", command=self.callbacks.get("import_magnettech1"),
                                     image=self.icon_epr,
                                     compound="left")
        self.menu_import.add_command(label="Magnettech newer (spe)", command=self.callbacks.get("import_magnettech2"),
                                     image=self.icon_epr,
                                     compound="left")
        # ------------ Separator
        self.menu_import.add_separator()

        # ------------ Shimadzu SPC
        self.menu_import.add_command(label="Shimadzu UV/VIS (spc)", command=self.callbacks.get("import_shimadzu_spc"), image=self.icon_shimadzu,
                                     compound="left")

        # ------------ Separator
        self.menu_import.add_separator()

        # ------------ ASCII Files
        self.menu_import.add_command(label="ASCII file", command=self.callbacks.get("import_ascii"), image=self.icon_import_ascii, compound="left")
        # ------------ Excel
        self.menu_import.add_command(label="MS Excel/LibreOffice Calc", command = self.callbacks.get("import_excel"), image = self.icon_import_excel, compound='left')
        #
        # # - SEPARATOR -
        self.menu_file.add_separator()
        #
        # Export
        self.menu_export = tk.Menu(self.menu_file, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                   activebackground=self.activebg, activeforeground=self.activefg,
                                   borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_file.add_cascade(label="Export", menu=self.menu_export, image=self.icon_export, compound="left")

        # - Export first
        self.menu_export.add_command(label="Export First", command=self.callbacks.get('export_first'), image=self.icon_export_first,
                                    compound="left")
        # # - Export group
        self.menu_export.add_command(label="Export Group", command=self.callbacks.get('export_group'), image=self.icon_export_group,
                                   compound="left", accelerator="Ctrl+Q")

        # - SEPARATOR -
        self.menu_file.add_separator()

        # - Quit
        self.menu_file.add_command(label="Quit", command=self.callbacks.get('close_application'), image = self.icon_exit, compound="left", accelerator="Ctrl+Q")

        # ''' Menu EDIT'''

        # #  EDIT
        self.menu_edit = tk.Menu(self.main_menu, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                  activebackground=self.activebg, activeforeground=self.activefg,
                                  borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.main_menu.add_cascade(label=" Edit ", menu=self.menu_edit)

        # - Data in spreadsheet
        self.menu_edit.add_command(label="Edit data in table", command=self.callbacks.get('edit_values_in_table'),
                                   image=self.icon_table, compound="left")

        # - Create from table
        self.menu_edit.add_command(label="Create data from table", command=self.callbacks.get('create_from_table'), image=self.icon_table, compound="left")

        # - Edit parameters
        self.menu_edit.add_command(label="Edit parameters", command = self.callbacks.get('edit_parameters'), image=self.icon_edit_par, compound="left")

        # - SEPARATOR -
        self.menu_edit.add_separator()

        # - Copy to clipboard
        self.menu_edit.add_command(label="Copy", command=self.callbacks.get('quick_copy'), image=self.icon_clipboard, compound="left", accelerator='Ctrl+C')

        # - Create from clipboard
        self.menu_edit.add_command(label="Paste", command=self.callbacks.get('quick_paste'),  image=self.icon_fromclipboard, compound="left", accelerator='Ctrl+V')

        # - SEPARATOR -
        self.menu_edit.add_separator()

        # - Delete selected data
        self.menu_edit.add_command(label="Delete selected data", command=self.callbacks.get('delete_selected_data'), image = self.icon_trash, compound="left")

        # - Notes
        self.menu_edit.add_command(label="Notes", command=self.callbacks.get('notes'), image = self.icon_notes, compound="left")

        # - Clear
        self.menu_clear = tk.Menu(self.menu_edit, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                 activebackground=self.activebg, activeforeground=self.activefg,
                                 borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_edit.add_cascade(label="Clear", menu=self.menu_clear, image = self.icon_clear, compound="left")

        # -------- Clear dataset
        self.menu_clear.add_command(label="Dataset", image = self.icon_trash, command=self.callbacks.get('clear_dataset'), compound="left")

        # -------- Clear result
        self.menu_clear.add_command(label="Result", image = self.icon_trashres, command=self.callbacks.get('clear_results'), compound="left")

        # - Groups
        self.menu_groups = tk.Menu(self.menu_edit, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                 activebackground=self.activebg, activeforeground=self.activefg,
                                 borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_edit.add_cascade(label="Groups", menu=self.menu_groups, image=self.icon_dropdown, compound="left")

        # -------- Assign First to group
        self.menu_groups.add_command(label="Assign First to group", command=self.callbacks.get('first_to_group'))

        # -------- Assign Second to group
        self.menu_groups.add_command(label="Assign Second to group", command=self.callbacks.get('second_to_group'))

        # - Graph Preferences
        self.menu_edit.add_command(label="Preferences", command = self.callbacks.get('preferences'), image=self.icon_graphPrefs, compound="left")

        ''' Menu ANALYSIS '''

        # ANALYSIS
        self.menu_analysis = tk.Menu(self.main_menu, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                            activebackground=self.activebg, activeforeground=self.activefg,
                            borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.main_menu.add_cascade(label="Analysis ", menu=self.menu_analysis)

        #  - Distance read
        self.menu_analysis.add_command(label="Calculate XY Distance", command=self.callbacks.get('xy_distance'),
                                       image=self.icon_distance, compound="left")

        #  - Integrate region
        self.menu_analysis.add_command(label="Integrate region", command=self.callbacks.get('integrate_region'),
                                  image=self.icon_integrate_region, compound="left")
        # #  - Statistics
        # self.menu_analysis.add_command(label="Statistics", command=self.app.quick_paste,
        #                            image=self.icon_statistics, compound="left")
        #

        ''' Menu MODIFICATIONS '''
        self.menu_modifications = tk.Menu(self.main_menu, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                     activebackground=self.activebg, activeforeground=self.activefg,
                                     borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.main_menu.add_cascade(label=" Modifications ", menu=self.menu_modifications)

        # - Normalize amplitude
        self.menu_modifications.add_command(label="Normalize amplitude", command=self.callbacks.get('normalize'),
                                       image=self.icon_normalize, compound="left")

        # - Trim data
        self.menu_modifications.add_command(label="Trim data", command=self.callbacks.get('trim_data'),
                                            image=self.icon_trimdata, compound="left")

        self.menu_modifications.add_separator()

        # - Subtract Polynomial baseline
        self.menu_modifications.add_command(label="Subtract polynomial baseline", command=self.callbacks.get('polynomial_baseline'),
                                            image=self.icon_baselineplynom, compound="left")

        # - Subtract Spline baseline
        self.menu_modifications.add_command(label="Subtract spline baseline", command=self.callbacks.get('spline_baseline'),
                                            image=self.icon_splinebaseline, compound="left")

        self.menu_modifications.add_separator()
        #
        # - Spectra subtraction
        self.menu_modifications.add_command(label="Spectra subtraction", command=self.callbacks.get('spectra_subtraction'),
                                           image=self.icon_spectrasubtract, compound="left")

        self.menu_modifications.add_separator()

        # - Filter
        self.menu_filters = tk.Menu(self.menu_modifications, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
                                  activebackground=self.activebg, activeforeground=self.activefg,
                                  borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        self.menu_modifications.add_cascade(label = "Filters", menu=self.menu_filters, image=self.icon_filter_general, compound='left')

        # --- Savitzky-Golay
        self.menu_filters.add_command(label="Savitzky-Golay Filter", command=self.callbacks.get('filter_savitzky_golay'),
                                            image=self.icon_sav_gol, compound="left")

        # --- FFT filter
        self.menu_filters.add_command(label="FFT filter", command = self.callbacks.get('filter_fft_lowpass'),
                                      image=self.icon_fftfilter, compound="left")

        # --- Pseudomodulation
        self.menu_filters.add_command(label="Pseudomodulation", command=self.callbacks.get('pseudomodulation'),
                                      image=self.icon_pseudomod, compound="left")

        # # - FFT
        # self.menu_modifications.add_command(label="FFT", command=self.app.fast_fourier_transform,
        #                                image=self.icon_fft, compound="left")
        #
        # ''' Menu EPR '''
        # self.menu_EPR = tk.Menu(self.main_menu, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
        #                                   activebackground=self.activebg, activeforeground=self.activefg,
        #                                   borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        #
        # self.main_menu.add_cascade(label="EPR ", menu=self.menu_EPR)
        #
        # # - B to g
        # self.menu_EPR.add_command(label="B to g value", command=self.app.epr_b_to_g,
        #                                     image=self.icon_btog, compound="left")
        #
        #
        # ''' Menu Tools '''
        # self.menu_tools = tk.Menu(self.main_menu, tearoff=1, bg=self.bg, fg=self.fg, font=self.font,
        #                          activebackground=self.activebg, activeforeground=self.activefg,
        #                          borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        #
        #
        # self.main_menu.add_cascade(label="Tools", menu=self.menu_tools)
        # self.menu_graphtools = tk.Menu(self.main_menu, tearoff=1, bg=self.bg, fg=self.fg, font=self.font,
        #                           activebackground=self.activebg, activeforeground=self.activefg,
        #                           borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        #
        # # - Graph tools
        # self.menu_tools.add_cascade(label="Graph tools", menu=self.menu_graphtools, image=self.icon_graphtools, compound="left")
        #
        # # ---- Clear selected range
        # self.menu_graphtools.add_command(label="Clear selected range", command=self.app.clear_selected_ranges,
        #                             image=self.icon_clearrange, compound="left")
        #
        #
        #
        # # - Create plot
        # self.menu_tools.add_command(label="Create plot", command=self.app.create_simple_static_plot,
        #                             image=self.icon_create_static_plot, compound="left")
        #
        # # - Delete plot
        # self.menu_tools.add_command(label="Delete plot", command=self.app.delete_simple_static_plot,
        #                             image=self.icon_delete_static_plot, compound="left")
        #
        # # -Separator
        # self.menu_tools.add_separator()
        #
        # # ---- ENTRIES IN menu_showPlots ARE GENERATED DYNAMICALLY
        #
        # ''' Menu HELP '''
        # self.menu_help = tk.Menu(self.main_menu, tearoff=0, bg=self.bg, fg=self.fg, font=self.font,
        #                         activebackground=self.activebg, activeforeground=self.activefg,
        #                         borderwidth=self.borderwidth, activeborderwidth=self.borderwidth)
        # #self.main_menu.add_cascade(label="Help", menu=self.menu_help, image=self.icon_dropdown, compound="left")
        # self.main_menu.add_cascade(label="Help", menu=self.menu_help)
        #
        # # - About
        # self.menu_help.add_command(label="About", command=self.app.quick_paste,
        #                                image=self.icon_statistics, compound="left")

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
            self.eleana.save_paths()
        list_for_menu = []
        i = 1
        for each in self.eleana.paths['last_projects']:
            item = Path(each)
            item = str(i) + '. ' + item.name
            list_for_menu.append(item)
            i += 1
        recent_menu = self.menu_recent
        recent_menu.delete(0, tk.END)
        icon_file = Path(self.eleana.paths['pixmaps'], 'project2.png')
        icon_clear = tk.PhotoImage(file=icon_file)

        for i, label in enumerate(list_for_menu):
            recent_menu.add_command(label=label, image = self.icon_project2, compound="left", command=lambda x=i: self.callbacks.get("load_project")(recent=x))

        # Separator and clear
        recent_menu.add_separator()
        recent_menu.add_command(label='Keep only last', image = self.icon_clear, compound="left", command=_clear_recent_list)

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

        if not self.eleana.settings.grapher['static_plots']:
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
    def __init__(self, master, eleana, gui_references, callbacks):
        self.eleana = eleana
        self.callbacks = callbacks
        self.master = master

        # References to GUI in the main applicationcwindow
        self.groupFrame = gui_references['groupFrame']
        self.sel_group = gui_references['sel_group']
        self.firstFrame = gui_references['firstFrame']
        self.sel_first =  gui_references['sel_first']
        self.firstStkFrame = gui_references['firstStkFrame']
        self.f_stk = gui_references["f_stk"]
        self.secondFrame = gui_references["seconFrame"]
        self.sel_second = gui_references["sel_second"]
        self.secondStkFrame = gui_references["secondStkFrame"]
        self.s_stk = gui_references["s_stk"]
        self.resultFrame = gui_references["resultFrame"]
        self.sel_result = gui_references["sel_result"]

        ''' Styling of the context menu '''
        self.bg = '#505050'
        self.fg = '#aaaaaa'
        self.font = ("Arial", 10)

        ''' References to Widgets '''
        # GROUPS
        self.groupFrame.bind("<Button-3>", self.show_context_menu_group)
        self.sel_group.bind("<Button-3>", self.show_context_menu_group)
        self.context_menu_group = tk.Menu(self.master, tearoff=0, bg=self.bg, fg=self.fg, font=self.font)

        # FIRST
        self.firstFrame.bind("<Button-3>", self.show_context_menu_first)
        self.sel_first.bind("<Button-3>", self.show_context_menu_first)
        self.context_menu_first = tk.Menu(self.master, tearoff=0, bg=self.bg, fg=self.fg, font = self.font)

        # FIRST STK
        self.firstStkFrame.bind("<Button-3>", self.show_context_menu_first_stk)
        self.f_stk.bind("<Button-3>", self.show_context_menu_first_stk)
        self.context_menu_first_stk = tk.Menu(self.master, tearoff=0, bg=self.bg, fg=self.fg, font=self.font)

        # SECOND
        self.secondFrame.bind("<Button-3>", self.show_context_menu_second)
        self.sel_second.bind("<Button-3>", self.show_context_menu_second)
        self.context_menu_second = tk.Menu(self.master, tearoff=0, bg=self.bg, fg=self.fg, font = self.font)

        # SECOND STK
        self.secondStkFrame.bind("<Button-3>", self.show_context_menu_second_stk)
        self.s_stk.bind("<Button-3>", self.show_context_menu_second_stk)
        self.context_menu_second_stk = tk.Menu(self.master, tearoff=0, bg=self.bg, fg=self.fg, font=self.font)

        # RESULT
        self.resultFrame.bind("<Button-3>", self.show_context_menu_result)
        self.sel_result.bind("<Button-3>", self.show_context_menu_result)
        self.context_menu_result = tk.Menu(self.master, tearoff=0, bg=self.bg, fg=self.fg, font = self.font)

        # Build context menu for FIRST
        self.build_menu_group()
        self.build_menu_first()
        self.build_menu_second()
        self.build_menu_result()
        self.build_menu_f_stk()
        self.build_menu_s_stk()

    def build_menu_group(self):
        '''This creates positions for FIRST context menu '''
        self.context_menu_group.add_command(label="Remove assignments to the group", command=self.callbacks.get('app.delete_group'))
        self.context_menu_group.add_command(label="Assign data to additional group", command=lambda: self.callbacks.get('data_to_other_group')(move=False))
        self.context_menu_group.add_command(label="Move data to other group", command=lambda: self.callbacks.get('data_to_other_group')(move=True))
        self.context_menu_group.add_command(label="Delete data assigned to the group",  command=self.callbacks.get('delete_data_from_group'))
        self.context_menu_group.add_command(label ="Convert whole group to a stack", command=lambda: self.callbacks.get('convert_group_to_stack')(all = True))
        self.context_menu_group.add_command(label="Convert selected to a stack", command=lambda: self.callbacks.get('convert_group_to_stack')(all = False))

    def build_menu_first(self):
        '''This creates positions for FIRST context menu '''
        self.context_menu_first.add_command(label="Rename", command=lambda: self.callbacks.get('rename_data')('first'))
        self.context_menu_first.add_command(label="Delete", command=lambda: self.callbacks.get('delete_data')('first'))
        self.context_menu_first.add_command(label="Duplicate", command=lambda: self.callbacks.get('duplicate_data')('first'))
        self.context_menu_first.add_command(label="Assign to group", command=self.callbacks.get('first_to_group'))
        self.context_menu_first.add_command(label="Convert stack to group", command=lambda: self.callbacks.get('stack_to_group')('first'))
        self.context_menu_first.add_command(label="Edit comment", command=lambda: self.callbacks.get('edit_comment')('first'))
        self.context_menu_first.add_command(label="Edit parameters", command = lambda: self.callbacks.get('edit_parameters')('first'))

    def build_menu_f_stk(self):
        '''This creates positions for FIRST STK context menu '''
        self.context_menu_first_stk.add_command(label="Delete", command=lambda: self.callbacks.get('delete_single_stk_data')('first'))


    def build_menu_second(self):
        '''This creates positions for SECOND context menu '''
        self.context_menu_second.add_command(label="Rename", command=lambda: self.callbacks.get('rename_data')('second'))
        self.context_menu_second.add_command(label="Delete", command=lambda: self.callbacks.get('delete_data')('second'))
        self.context_menu_second.add_command(label="Duplicate", command=lambda: self.callbacks.get('duplicate_data')('second'))
        self.context_menu_second.add_command(label="Assign to group", command=self.callbacks.get('second_to_group'))
        self.context_menu_second.add_command(label="Convert stack to group", command=lambda: self.callbacks.get('stack_to_group')('second'))
        self.context_menu_second.add_command(label="Edit comment", command=lambda: self.callbacks.get('edit_comment')('second'))
        self.context_menu_second.add_command(label="Edit parameters", command=lambda: self.callbacks.get('edit_parameters')('second'))

    def build_menu_s_stk(self):
        '''This creates positions for SECOND STK context menu '''
        self.context_menu_second_stk.add_command(label="Delete", command=lambda: self.callbacks.get('delete_single_stk_data')('second'))


    def build_menu_result(self):
        '''This creates positions for SECOND context menu '''
        self.context_menu_result.add_command(label="Rename", command=lambda: self.callbacks.get('rename_data')('result'))
        self.context_menu_result.add_command(label="Delete", command=lambda: self.callbacks.get('delete_data')('result'))
        self.context_menu_second.add_command(label="Duplicate", command=lambda: self.callbacks.get('duplicate_data')('result'))

    def show_context_menu_group(self, event):
        self.context_menu_group.tk_popup(event.x_root, event.y_root)

    def show_context_menu_first(self, event):
        self.context_menu_first.tk_popup(event.x_root, event.y_root)

    def show_context_menu_first_stk(self, event):
        self.context_menu_first_stk.tk_popup(event.x_root, event.y_root)

    def show_context_menu_second_stk(self, event):
        self.context_menu_second_stk.tk_popup(event.x_root, event.y_root)


    def show_context_menu_second(self, event):
        self.context_menu_second.tk_popup(event.x_root, event.y_root)

    def show_context_menu_result(self, event):
        self.context_menu_result.tk_popup(event.x_root, event.y_root)
        print('Context menu')
