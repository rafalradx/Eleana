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

# Import External modules required
import numpy as np
import pandas

# Import modules from ./modules folder
import pygubu
from CTkListbox import CTkListbox
from CTkMessagebox import CTkMessagebox
from CTkScrollableDropdown import CTkScrollableDropdown
from widgets.CTkSpinbox import CTkSpinbox


# Import Eleana specific classes
from Eleana import Eleana
from LoadSave import Load, Save, Export
from Init import Init
from Grapher import Grapher
from Update import Update
from Menu import ContextMenu, MainMenu
from Sounds import Sound
from Error import Error
from CommandProcessor import CommandProcessor
from DataClasses import BaseDataModel
from Error import Error
from IconToWidget import IconToWidget

# Import Eleana subprograms and windows
# append.(['name of instance without self., 'Command to close']

list_of_subprogs = []
from filter_fft.fft_filter import FFTFilter
from filter_savitzky_golay.sav_gol import SavGol
from edit_values_in_table.edit_values_in_table import EditValuesInTable
from pseudomodulation.pseudomodulation import PseudoModulation
from fft.fast_fourier_transform import FastFourierTransform
from spectra_subtraction.spectra_subtration import SpectraSubtraction

#list_of_subprogs.append(['edit_values_in_table', 'cancel'])
from EPR_B_to_g.B_to_g import EPR_B_to_g
#list_of_subprogs.append(['subprog_epr_b_to_b', 'cancel'])
from trim_data.Trim_data import TrimData
#list_of_subprogs.append(['subprog_trim_data', 'cancel'])
from spline_baseline.Spline_baseline import SplineBaseline
#list_of_subprogs.append(['subprog_spline_baseline', 'cancel'])
from polynomial_baseline.Polynomial_baseline import PolynomialBaseline
#list_of_subprogs.append(['subprog_polynomial_baseline', 'cancel'])
from distance_read.Distance_read import DistanceRead
#list_of_subprogs.append(['xy_distance', 'cancel'])
from integrate_region.IntegrateRegion import IntegrateRegion
#list_of_subprogs.append(['integrate_region', 'cancel'])
from normalize.normalize_2 import Normalize
#list_of_subprogs.append(['normalize', 'cancel'])
from group_edit.add_group import Groupcreate
#list_of_subprogs.append(['group_create', 'cancel'])
from group_edit.assign_to_group import Groupassign
#list_of_subprogs.append(['group_assign', 'cancel'])
from user_input.single_dialog import SingleDialog
#list_of_subprogs.append(['single_dialog', 'cancel'])
from select_data.select_data import SelectData
#list_of_subprogs.append(['select_items', 'cancel'])
from select_data.select_items import SelectItems
#list_of_subprogs.append(['select_data', 'cancel'])
from notepad.notepad import Notepad
#list_of_subprogs.append(['notepad', 'cancel'])
from table.table import CreateFromTable
#list_of_subprogs.append(['spreadsheet', 'cancel'])
from edit_parameters.edit_parameters import EditParameters
#list_of_subprogs.append(['edit_par', 'cancel'])
from modify.modify import ModifyData
#list_of_subprogs.append(['modify_data', 'cancel'])
from group_edit.move_to_group import MoveToGroup
#list_of_subprogs.append(['move_to_group', 'cancel'])
from preferences.preferences import PreferencesApp
#list_of_subprogs.append(['prefereces', 'cancel'])
from group_edit.stack_to_group import StackToGroup
#list_of_subprogs.append(['convert_stack_to_group', 'cancel'])

# Widgets used by main application
from widgets.CTkHorizontalSlider import CTkHorizontalSlider

def check_busy(method):

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self.mainwindow.configure(cursor="watch")
        if self.eleana.busy:
            if self.eleana.devel_mode:
                print(f"{Path(__file__).name}, {method.__name__}: self.eleana.busy = True")
            return
        result = method(self, *args, **kwargs)
        self.mainwindow.configure(cursor="")
        self.after_gui_action(by_method = method.__name__)
        return result
    return wrapper

class MainApp:
    def __init__(self, eleana_instance, command_processor, master=None):
        # Initialize eleana
        self.eleana = eleana_instance
        self.notify = self.eleana.notify_on
        self.commandprocessor = command_processor
        self.devel = DEVEL

        # START BUILDER
        self.builder = builder = pygubu.Builder()
        self.builder.add_resource_path(PROJECT_PATH)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("Eleana", master)
        self.mainwindow.iconify()
        self.mainwindow.withdraw()
        self.builder.connect_callbacks(self)
        # END OF PYGUBU BUILDER

        # Create references to Widgets and Frames
        self.switch_comparison = builder.get_object("switch_comp_view", self.mainwindow)
        self.sel_group = builder.get_object("sel_group", self.mainwindow)
        self.sel_first = builder.get_object("sel_first", self.mainwindow)
        self.sel_second = builder.get_object("sel_second", self.mainwindow)
        self.sel_result = builder.get_object("sel_result", self.mainwindow)

        # Frames must be configured due to a bug in Pygubu
        self.selectionsFrame = builder.get_object("selectionsFrame", self.mainwindow)
        self.groupFrame = builder.get_object("groupFrame", self.mainwindow)
        self.rightFrame = builder.get_object("rightFrame", self.mainwindow)
        self.graphButtons = builder.get_object('graphButtons', self.mainwindow)

        self.listFrame = ctk.CTkFrame(master=self.selectionsFrame)
        self.firstFrame = builder.get_object("firstFrame", self.mainwindow)
        self.secondFrame = builder.get_object("secondFrame", self.mainwindow)
        self.resultFrame = builder.get_object("resultFrame", self.mainwindow)
        self.resultStkFrame = builder.get_object("resultStkFrame", self.mainwindow)
        self.firstStkFrame = builder.get_object("firstStkFrame", self.mainwindow)
        self.secondStkFrame = builder.get_object("secondStkFrame", self.mainwindow)
        self.firstComplex = builder.get_object("firstComplex", self.mainwindow)
        self.secondComplex = builder.get_object("secondComplex", self.mainwindow)
        self.resultComplex = builder.get_object("resultComplex", self.mainwindow)
        self.graphFrame = builder.get_object('graphFrame', self.mainwindow)
        self.swapFrame = builder.get_object('swapFrame', self.mainwindow)
        self.f_stk = builder.get_object('f_stk', self.mainwindow)
        self.s_stk = builder.get_object('s_stk', self.mainwindow)
        self.r_stk = builder.get_object('r_stk', self.mainwindow)
        self.btn_clear_results = builder.get_object('btn_clear_results', self.mainwindow)
        self.check_first_show = builder.get_object('check_first_show', self.mainwindow)
        self.check_second_show = builder.get_object('check_second_show', self.mainwindow)
        self.check_result_show = builder.get_object('check_result_show', self.mainwindow)
        self.annotationsFrame = builder.get_object('annotationsFrame', self.mainwindow)

        # Modification Panel FIRST
        self.first_modFrame = builder.get_object('first_modFrame', self.mainwindow)
        self.first_mod_panel_1 = builder.get_object('first_mod_panel_1', self.mainwindow)
        self.first_mod_panel_1.grid_remove()
        self.first_mod_panel_2 = builder.get_object('first_mod_panel_2', self.mainwindow)
        self.first_mod_panel_2.grid_remove()
        self.first_mod_panel_3 = builder.get_object('first_mod_panel_3', self.mainwindow)
        self.first_mod_panel_3.grid_remove()
        self.first_mod_panel_4 = builder.get_object('first_mod_panel_4', self.mainwindow)
        self.first_mod_panel_4.grid_remove()
        self.first_mod_panel_5 = builder.get_object('first_mod_panel_5', self.mainwindow)
        self.first_mod_panel_5.grid_remove()
        self.first_mod_panel_6 = builder.get_object('first_mod_panel_6', self.mainwindow)
        self.first_mod_panel_6.grid_remove()
        self.first_mod_panel_7 = builder.get_object('first_mod_panel_7', self.mainwindow)
        self.first_mod_panel_7.grid_remove()
        self.first_mod_panel_8 = builder.get_object('first_mod_panel_8', self.mainwindow)
        self.first_mod_panel_8.grid_remove()

        # Place CTkSpinboxex
        self.ctkframe8  = builder.get_object('ctkframe8', self.mainwindow)
        self.first_mod_panel_1 = CTkSpinbox(master = self.ctkframe8, min_value=-1000000000, max_value=1000000000, step_value=1,  scroll_value = 1)
        self.first_mod_panel_1.grid(row=0, column=1, sticky="ew")
        self.first_mod_panel_2 = CTkSpinbox(master=self.ctkframe8, min_value=0.000000001, max_value=10000000000, command = self.first_mod_step_settings, step_value=1, scroll_value=0)
        self.first_mod_panel_2.grid(row=1, column=1, sticky="ew")
        self.first_mod_panel_2.set(1)

        self.ctkframe23 = builder.get_object('ctkframe23', self.mainwindow)
        self.first_mod_panel_3 = CTkSpinbox(master=self.ctkframe23, min_value=-1000000000, max_value=1000000000, step_value=1, scroll_value=1)
        self.first_mod_panel_3.grid(row=0, column=1, sticky="ew")
        self.first_mod_panel_4 = CTkSpinbox(master=self.ctkframe23, min_value=0.000000001, max_value=10000000000, command = self.first_mod_step_settings, step_value=1, scroll_value=0)
        self.first_mod_panel_4.grid(row=1, column=1, sticky="ew")
        self.first_mod_panel_4.set(1)

        self.ctkframe19 = builder.get_object('ctkframe19', self.mainwindow)
        self.first_mod_panel_5 = CTkSpinbox(master=self.ctkframe19, min_value=0, max_value=1000000, step_value=1, scroll_value=1)
        self.first_mod_panel_5.grid(row=0, column=1, sticky="ew")
        self.first_mod_panel_6 = CTkSpinbox(master=self.ctkframe19, min_value=0.000000001, max_value=10000000000, command = self.first_mod_step_settings, step_value=1, scroll_value=0)
        self.first_mod_panel_6.grid(row=1, column=1, sticky="ew")
        self.first_mod_panel_6.set(1)

        self.ctkframe24 = builder.get_object('ctkframe24', self.mainwindow)
        self.first_mod_panel_7 = CTkSpinbox(master=self.ctkframe24, min_value=0, max_value=1000000, step_value=1, scroll_value=1)
        self.first_mod_panel_7.grid(row=0, column=1, sticky="ew")
        self.first_mod_panel_8 = CTkSpinbox(master=self.ctkframe24, min_value=0.000000001, max_value=10000000000, command = self.first_mod_step_settings, step_value=1, scroll_value=0)
        self.first_mod_panel_8.grid(row=1, column=1, sticky="ew")
        self.first_mod_panel_8.set(1)

        # Hide FIRST modifications
        self.first_modFrame.grid_remove()
        self.btn_toggle_first_mod = builder.get_object("btn_toggle_first_mod", self.mainwindow)

        # Graph Buttons
        self.check_autoscale_x = builder.get_object('check_autoscale_X', self.mainwindow)
        self.check_autoscale_y = builder.get_object('check_autoscale_Y', self.mainwindow)
        self.check_log_x = builder.get_object('check_log_x', self.mainwindow)
        self.check_log_y = builder.get_object('check_log_y', self.mainwindow)
        self.check_indexed_x = builder.get_object('check_indexed_x', self.mainwindow)
        self.sel_cursor_mode = builder.get_object('sel_cursor_mode', self.mainwindow)
        self.check_invert_x = builder.get_object('check_invert_x', self.mainwindow)
        self.btn_clear_cursors = builder.get_object("btn_clear_cursors", self.mainwindow)
        self.info = builder.get_object('info', self.mainwindow)
        self.infoframe = builder.get_object('infoframe', self.mainwindow)
        self.infoframe.grid_remove()
        self.btn_clear_cursors.grid_remove()
        self.annotationsFrame.grid_remove()

        # Command line
        self.command_line = builder.get_object('command_line', self.mainwindow)
        self.command_line.bind("<Return>", self.execute_command)
        self.command_line.bind("<Up>", self.execute_command)
        self.command_line.bind("<Down>", self.execute_command)
        self.command_history = {'index': 0, 'lines': []}
        self.log_field = builder.get_object('log_field', self.mainwindow)

        # Paned windows
        self.panedwindow2 = builder.get_object('panedwindow2', self.mainwindow)
        self.panedwindow4 = builder.get_object('panedwindow4', self.mainwindow)
        self.pane5 = builder.get_object('pane5', self.mainwindow)
        self.pane9 = builder.get_object('pane9', self.mainwindow)
        #self.pane6 = builder.get_object('pane6', self.mainwindow)

        # Keyboard bindings
        self.mainwindow.bind("<Control-c>", self.copy_to_clipboard)
        self.mainwindow.bind("<Control-s>", self.save_current)
        self.mainwindow.bind("<Control-q>", self.close_application)
        self.mainwindow.bind("<Control-o>", self.load_project)
        self.mainwindow.bind("<Control-v>", self.quick_paste)

        # This keeps the information if any information or dialog should be displayed.
        # This is useful to constantly display the same information in a loop etc.
        self.info_show = True
        self.repeated_items = []

        # Comparison view
        self.comparison_settings = {'vsep': 0, 'hsep': 0, 'indexes': (), 'v_factor': '1', 'h_factor': '1'}

        # Ctk styles
        self.gui_appearence = 'light'
        self.color_theme = 'dark-blue'

        # Set icons for buttons and widgets
        IconToWidget.eleana(app = self)

    def scrollable_dropdown(self, selection, combobox):
        ''' Interconnects CTkScrollableDropdown to standard CTkCombobox'
            This function translates the events of item selection to event
            of standard combobox selection
        '''
        if combobox == 'sel_first':
            self.first_selected(selection)
            self.sel_first.set(selection)
        elif combobox == 'f_stk':
            self.f_stk_selected(selection)
            self.f_stk.set(selection)
        elif combobox == 'sel_second':
            self.second_selected(selection)
            self.sel_second.set(selection)
        elif combobox == 's_stk':
            self.s_stk_selected(selection)
            self.s_stk.set(selection)
        elif combobox == 'sel_result':
            self.result_selected(selection)
            self.sel_result.set(selection)
        elif combobox == 'r_stk':
            self.r_stk_selected(selection)
            self.r_stk.set(selection)

        self.mainwindow.focus_set()

    def create_f_stk(self):
        #self.f_stk = self.builder.get_object('f_stk', self.mainwindow)
        self.builder.connect_callbacks()

    def set_grapher(self, grapher):
        self.grapher = grapher

    def set_update(self, update):
        self.update = update

    def set_pane_height(self):
        self.mainwindow.update_idletasks()
        self.panedwindow2.sashpos(0, 700)
        self.panedwindow4.sashpos(0, 400)
        self.pane5.sashpos(0, 1100)
        self.mainwindow.update_idletasks()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def run(self):
        self.mainwindow.after(100, self.set_pane_height)
        self.mainwindow.deiconify()
        self.mainwindow.mainloop()

    def after_gui_action(self, by_method = None):
        if self.eleana.active_subprog is None:
            if self.eleana.devel_mode:
                print("Subprog Inactive")
        else:
            self.eleana.active_subprog.finish_action(by_method)


    ''' *********************************************
    *              COMPARISON VIEW                  *
    **********************************************'''

    def comparison_view(self):
        self.info_show = True
        self.repeated_items = []
        comparison_mode = bool(self.switch_comparison.get())
        if comparison_mode:
            self.graphButtons.grid_remove()
            self.firstFrame.grid_remove()
            self.secondFrame.grid_remove()
            self.resultFrame.grid_remove()
            self.swapFrame.grid_remove()

            self.listFrame.grid(column=0, row=2, rowspan=3, sticky = "nsew")
            self.listbox = CTkListbox(self.listFrame, command=self.list_selected, multiple_selection=True, height=400)
            self.listbox.grid(column=0, columnspan=1, rowspan=4, padx=4, pady=4, row=0, sticky="nsew")

            self.ver_slider = CTkHorizontalSlider('Vertical separation', 'vsep', [0, 1], self.listFrame, self)
            self.ver_slider.grid(column=0, columnspan=1, rowspan=3, padx=4, pady=4, row=5, sticky="nsew")

            self.hor_slider = CTkHorizontalSlider('Horizontal separation', 'hsep', [-1, 1], self.listFrame, self)
            self.hor_slider.grid(column=0, columnspan=1, rowspan=3, padx=4, pady=4, row=8, sticky="nsew")
            self.ver_slider.factor.delete(0, 'end')
            self.ver_slider.factor.insert(0, self.comparison_settings['v_factor'])
            self.hor_slider.factor.delete(0, 'end')
            self.hor_slider.factor.insert(0, self.comparison_settings['h_factor'])

            # Get names from group to be used for the list
            group = self.eleana.selections['group']
            names_nr = []
            indexes = []
            if group == 'All':
                i = 0
                while i < len(self.eleana.dataset):
                    names_nr.append(self.eleana.dataset[i].name_nr)
                    indexes.append(i)
                    i += 1
            else:
                indexes = self.eleana.assignmentToGroups[group]
                for i in indexes:
                    names_nr.append(self.eleana.dataset[i].name_nr)
            i = 0
            while i < len(names_nr) - 1:
                self.listbox.insert(indexes[i], names_nr[i])
                i += 1
            try:
                self.listbox.insert("END", names_nr[i])
            except:
                pass
            if len(self.comparison_settings['indexes']) > 0:
                for each in self.comparison_settings['indexes']:
                    self.listbox.activate(each)
            self.list_selected()
        else:
            self.listFrame.grid_remove()
            self.graphButtons.grid()
            self.firstFrame.grid()
            self.secondFrame.grid()
            self.swapFrame.grid()
            if len(self.eleana.results_dataset) > 0:
                self.resultFrame.grid()
            self.grapher.plot_graph()

    def separate_plots_by(self, direction=None, value=None):
        self.mainwindow.config(cursor="watch")
        if direction != None or value != None:
            self.comparison_settings[direction] = value
        vsep = np.array([0])
        vstep = self.comparison_settings['vsep']
        hsep = np.array([0])
        hstep = self.comparison_settings['hsep']
        i = 1
        while i < len(self.comparison_settings['indexes']):
            next_h = i * hstep
            next_v = i * vstep
            vsep = np.append(vsep, next_v)
            hsep = np.append(hsep, next_h)
            i += 1
        self.grapher.plot_comparison(self.comparison_settings['indexes'], vsep, hsep)
        self.comparison_settings['v_factor'] = self.ver_slider.factor.get()
        self.comparison_settings['h_factor'] = self.hor_slider.factor.get()
        self.mainwindow.config(cursor='arrow')

    def list_selected(self, selected_items=None):
        if selected_items != None:
            previous_selection = self.comparison_settings['indexes']
            self.repeated_items.extend(selected_items)
            for each in selected_items:
                index = int(self.eleana.get_index_by_name(each))
                type = self.eleana.dataset[index].type
                name_nr = self.eleana.dataset[index].name_nr
                if name_nr in set(self.repeated_items):
                    self.info_show = True
                if type == 'stack 2D' and self.info_show:
                    info = 'Data "' + name_nr + '" is a 2D stack. You need to convert the stack into a group to display it.'
                    CTkMessagebox(master = self.mainwindow, title="", message=info)
                    selected_stack = self.listbox.curselection()
                    difference = set(selected_stack) - set(previous_selection)
                    difference = list(difference)
                    if len(difference) > 0:
                        self.listbox.deselect(difference[0])
                    self.info_show = False
                    return
            items_list = []
            for each in selected_items:
                items_list.append(int(self.eleana.get_index_by_name(each)))
            items_list.sort()
            self.comparison_settings['indexes'] = tuple(items_list)
            self.separate_plots_by()
        else:
            self.comparison_settings['indexes'] = ()
            self.grapher.clear_plot()

    # Handling the FIRST MODIFICATION PANNEL
    # --------------------------------------------

    def toggle_first_mod_panel(self):
        ''' Hides of shows the first_modFrame upon clicking the toggle button '''
        if self.first_modFrame.winfo_ismapped():
            self.first_modFrame.grid_remove()
            self.btn_toggle_first_mod.configure(text = "[---]")
        else:
            self.first_modFrame.grid()
            self.btn_toggle_first_mod.configure(text=" [-] ")
            Error.show(info = "This is not implemented yet")

    def first_mod_step_settings(self, value):
        ''' When modification panel is on an step is changed then it sets the step values
            are set to spinboxes
        '''
        def _set_ranges(widget):
            v = widget.get()
            step = widget.step_value
            if v == step:
                return False
            difference = v - step
            if difference > 0:
                new_v = (v - step)  * 10
            elif v == 0:
                new_v = 1
            else:
                new_v = (v + step) / 10
            if new_v > 1:
                new_v = int(new_v)
            widget.step_value = new_v
            widget.set(value = new_v)
            return True

        widget_list = (self.first_mod_panel_2, self.first_mod_panel_4, self.first_mod_panel_6, self.first_mod_panel_8)
        for widget in widget_list:
            result = _set_ranges(widget=widget)
            if result:
                return
    # -------  END of FIRST MODIFICATION PANEL --------


    ''' *********************************************
    *              COMBOBOX SELECTIONS              *
    **********************************************'''

    @check_busy
    def group_down_clicked(self):
        current_group = self.sel_group.get()
        group_list = self.sel_group._values
        index = group_list.index(current_group)
        if index == 0:
            return
        index -= 1
        new_group = group_list[index]
        self.sel_group.set(new_group)
        self.group_selected(new_group)

    @check_busy
    def group_up_clicked(self):
        current_group = self.sel_group.get()
        group_list = self.sel_group._values
        index = group_list.index(current_group)
        if index == len(group_list) - 1:
            return
        index += 1
        new_group = group_list[index]
        self.sel_group.set(new_group)
        self.group_selected(new_group)

    @check_busy
    def group_selected(self, value):
        self.eleana.set_selections('group', value)
        update.all_lists()
        self.sel_first.set('None')
        self.sel_second.set('None')
        self.eleana.set_selections('first', - 1)
        self.eleana.set_selections('second', -1)
        update.gui_widgets()
        self.grapher.plot_graph()
        self.comparison_view()

    @check_busy
    def delete_group(self):
        if self.eleana.busy:
            if self.eleana.devel_mode:
                print('delete_group_clicked - blocked by self.eleana.busy')
            return
        current_group = self.eleana.selections['group']
        if current_group == 'All':
            info = CTkMessagebox(master = self.mainwindow,
                                 title='',
                                 message="The group 'All' cannot be removed.",
                                 icon='cancel')
            return
        av_data = self.sel_first._values
        av_data.pop(0)
        #self.select_data = SelectData(master=app.mainwindow, title='Select data', group=self.eleana.selections['group'],
        #                              items=av_data)
        #names = self.select_data.get()

        select_data = SelectData(master=app.mainwindow, title='Select data', group=self.eleana.selections['group'],
                                      items=av_data)
        names = select_data.get()

        if not names:
            return
        indexes = self.get_indexes_by_name(names)
        if not indexes:
            return
        for index in indexes:
            data_groups = self.eleana.dataset[index].groups
            if current_group in data_groups:
                data_groups.remove(current_group)
                self.eleana.dataset[index].groups = data_groups
        update.dataset_list()
        update.groups()
        update.all_lists()
        if current_group not in self.eleana.assignmentToGroups['<group-list/>']:
            self.sel_group.set('All')
            self.eleana.selections['group'] = 'All'

    @check_busy
    def data_to_other_group(self, move = True):
        if self.eleana.selections['group'] == 'All' and move:
            info = CTkMessagebox(master = self.mainwindow,
                                 title='', message="Data from the 'All' group cannot be moved to another group. However, you can make an additional assignment.",
                                icon='cancel')
            return

        # Select data
        av_data = self.sel_first._values
        av_data.pop(0)
        self.select_data = SelectData(master=self.mainwindow, title='Select data', group=self.eleana.selections['group'],
                                      items=av_data)
        names = self.select_data.get()
        if not names:
            return
        indexes = self.get_indexes_by_name(names)
        if not indexes:
            return
        move_to_group = MoveToGroup(self.mainwindow, self)
        new_group = move_to_group.get()

        if new_group == None:
            return
        elif new_group == 'All' and move:
            info = CTkMessagebox(master = self.mainwindow, title = '', message = "You cannot move data from the group 'All' to another one.", icon='cancel')
            return

        # Replace current_group with new_group
        current_group = self.eleana.selections['group']
        for index in indexes:
            groups = self.eleana.dataset[index].groups
            if current_group in groups and move:
                position = groups.index(current_group)
                groups[position] = new_group
                self.eleana.dataset[index].groups = groups
            elif new_group in groups and not move:
                return
            elif new_group not in groups and not move:
                groups.append(new_group)
                self.eleana.dataset[index].groups = groups
            else:
                return
        update.dataset_list()
        update.groups()
        update.all_lists()
        self.sel_group.set('All')

    @check_busy
    def delete_data_from_group(self, skip_questions=False):
        group = self.eleana.selections['group']
        data_indexes = self.eleana.assignmentToGroups.get(group, None)
        if group == 'All' and not skip_questions:
            info = CTkMessagebox(master = self.mainwindow, title = 'Delete Data from Group', message = 'You cannot delete data from the group "All". Please use "Delete Dataset" instead.', icon = 'cancel' )
        elif not skip_questions:
            info = CTkMessagebox(master = self.mainwindow, title= 'Delete Data from Group', icon="warning", option_1="Cancel", option_2="Delete", message = f'Are you sure you want to delete data from the group "{group}"?')
            response = info.get()
            if response == 'Cancel' or not data_indexes:
                return
        if data_indexes is None:
            return
        data_indexes = sorted(data_indexes, reverse=True)
        for index in data_indexes:
            self.eleana.dataset.pop(index)
        group_list = self.eleana.assignmentToGroups['<group-list/>']
        if group in group_list:
            group_list.remove(group)
            self.eleana.assignmentToGroups['<group-list/>'] = group_list
        update.dataset_list()
        update.groups()
        self.sel_group.set('All')
        self.sel_first.set('None')
        self.eleana.selections['first'] = -1
        self.sel_second.set('None')
        self.eleana.selections['second'] = -1
        update.all_lists()
        update.gui_widgets()

    @check_busy
    def convert_group_to_stack(self, all = False):
        if all:
            # Convert whole data in the group to a stack
            indexes = self.eleana.get_indexes_from_group()
        else:
            # Ask to select
            av_data = self.sel_first._values
            av_data.pop(0)
            selected_data = SelectData(master=app.mainwindow, title='Select data', group=self.eleana.selections['group'],
                                      items=av_data)
            response = selected_data.get()
            if response == None:
                return
            indexes = [self.eleana.get_index_by_name(i) for i in response]
        # Check if data are of the same type
        template = self.eleana.dataset[indexes[0]]
        new_stack = {}
        stk_names = []
        list_of_y = []
        for i in indexes:
            compared = self.eleana.dataset[i]
            stk_name = str(i+1) + '_' + template.name
            stk_names.append(stk_name)
            y = compared.y
            list_of_y.append(y)
            parameters = template.parameters
            comment = ''
            if template.type != compared.type:
                info = CTkMessagebox(master = self.mainwindow, title='Convert to a Stack', message='At least one of the data elements is of a different type (for example, 2D and 3D).')
                return
            if template.complex != compared.complex:
                info = CTkMessagebox(master = self.mainwindow, title='Convert to a Stack', message='At least one of the data elements has a different type of numbers (for example, real and complex).')
                return
            if template.x.size != compared.x.size:
                info = CTkMessagebox(master = self.mainwindow, title='Convert to a Stack', message='At least one of the data elements has a different number of points. You can convert the data to a stack only if all of them are the same size.')
                return
            if not np.array_equal(template.x, compared.x):
                dialog = CTkMessagebox(master = self.mainwindow, title="Convert to Stack", message="The x-axes of the selected items are not identical. You may still proceed, but the differing axes will be replaced with the x-axis from the first item in the list.", icon="warning", option_1="Cancel", option_2="OK")
                response = dialog.get()
                if response == 'Cancel':
                    return
        # Now create a stack
        name = self.eleana.selections['group'] + ':TO_STACK'
        x = template.x
        y = np.array(list_of_y)
        new_stack = {'parameters':parameters,
                'name':name,
                'stk_names':stk_names,
                'x':x,
                'y':y,
                'origin':'converted from group',
                'type':'stack 2D',
                'name_nr':'',
                'comment':'',
                'complex':template.complex,
                'groups':'All',
                }
        created_stack = BaseDataModel.from_dict(new_stack)
        self.add_to_results(created_stack)

    @check_busy
    def first_show(self):
        self.eleana.set_selections('f_dsp', bool(self.check_first_show.get()))
        selection = self.sel_first.get()
        if selection == 'None':
            return
        self.first_selected(selection)
        self.grapher.plot_additional_curves()

    @check_busy
    def first_down_clicked(self):
        current_position = self.sel_first.get()
        list_of_items = self.sel_first._values
        if current_position == 'None':
            return
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_first not found')
            return
        try:
            new_position = list_of_items[index - 1]
            self.sel_first.set(new_position)
            self.first_selected(new_position)
        except IndexError:
            return

    @check_busy
    def first_up_clicked(self):
        current_position = self.sel_first.get()
        list_of_items = self.sel_first._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            return
        try:
            new_position = list_of_items[index + 1]
            self.sel_first.set(new_position)
            self.first_selected(new_position)
        except IndexError:
            return

    @check_busy
    def first_complex_clicked(self, value):
        self.eleana.set_selections('f_cpl', value)
        self.grapher.plot_graph()

    @check_busy
    def first_selected(self, selected_value_text):
        if selected_value_text == 'None':
            self.eleana.set_selections('first', -1)
            self.firstComplex.grid_remove()
            self.firstStkFrame.grid_remove()
            self.grapher.plot_graph()
            return
        i = 0
        while i < len(self.eleana.dataset):
            name = self.eleana.dataset[i].name_nr
            if name == selected_value_text:
                self.eleana.set_selections('first', i)
                self.sel_first.set(name)
                break
            i += 1
        update.list_in_combobox('sel_first')
        update.list_in_combobox('f_stk')
        if self.eleana.dataset[self.eleana.selections['first']].complex:
            self.firstComplex.grid()
        else:
            self.firstComplex.grid_remove()
        self.eleana.selections['f_stk'] = 0
        self.grapher.plot_graph()

    @check_busy
    def f_stk_selected(self, selected_value_text):
        if selected_value_text in self.f_stk._values:
            index = self.f_stk._values.index(selected_value_text)
            self.eleana.set_selections('f_stk', index)
        else:
            return
        self.grapher.plot_graph()

    @check_busy
    def f_stk_up_clicked(self):
        current_position = self.f_stk.get()
        list_of_items = self.f_stk._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in f_stk not found.')
            return
        try:
            new_position = list_of_items[index + 1]
            self.f_stk.set(new_position)
            self.eleana.set_selections('f_stk', index + 1)
        except IndexError:
            return
        self.grapher.plot_graph()

    @check_busy
    def f_stk_down_clicked(self):
        current_position = self.f_stk.get()
        list_of_items = self.f_stk._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in f_stk not found.')
            return
        if index == 0:
            return
        try:
            new_position = list_of_items[index - 1]
            self.f_stk.set(new_position)
            self.eleana.set_selections('f_stk', index - 1)
        except IndexError:
            return
        self.grapher.plot_graph()

    @check_busy
    def modify_first(self):
        self.modify('first')

    @check_busy
    def modify_second(self):
        self.modify('second')

    @check_busy
    def modify(self, which=None):
        if len(self.eleana.dataset) == 0:
            info = CTkMessagebox(master = self.mainwindow, title='', message='Empty dataset')
            return
        if not which:
            which = 'first'

        modify_data = ModifyData(self, which)
        response = modify_data.get()

    @check_busy
    def second_show(self):
        self.eleana.set_selections('s_dsp', bool(self.check_second_show.get()))
        selection = self.sel_second.get()
        if selection == 'None':
            return
        self.second_selected(selection)

    @check_busy
    def second_selected(self, selected_value_text):
        if selected_value_text == 'None':
            self.eleana.set_selections('second', -1)
            self.secondComplex.grid_remove()
            self.secondStkFrame.grid_remove()
            self.grapher.plot_graph()
            return
        i = 0
        while i < len(self.eleana.dataset):
            name = self.eleana.dataset[i].name_nr
            if name == selected_value_text:
                self.eleana.set_selections('second', i)
                break
            i += 1
        update.list_in_combobox('sel_second')
        update.list_in_combobox('s_stk')
        if self.eleana.dataset[self.eleana.selections['second']].complex:
            self.secondComplex.grid()
        else:
            self.secondComplex.grid_remove()
        self.eleana.selections['s_stk'] = 0
        self.grapher.plot_graph()

    @check_busy
    def second_down_clicked(self):
        current_position = self.sel_second.get()
        list_of_items = self.sel_second._values
        if current_position == 'None':
            return
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_second not found.')
            return
        try:
            new_position = list_of_items[index - 1]
            self.sel_second.set(new_position)
            self.second_selected(new_position)
        except IndexError:
            return

    @check_busy
    def second_up_clicked(self):
        current_position = self.sel_second.get()
        list_of_items = self.sel_second._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_second not found.')
            return
        try:
            new_position = list_of_items[index + 1]
            self.sel_second.set(new_position)
            self.second_selected(new_position)
        except IndexError:
            return

    def s_stk_selected(self, selected_value_text):
        if selected_value_text in self.s_stk._values:
            index = self.s_stk._values.index(selected_value_text)
            self.eleana.set_selections('s_stk', index)
        else:
            return
        self.grapher.plot_graph()

    @check_busy
    def s_stk_up_clicked(self):
        current_position = self.s_stk.get()
        list_of_items = self.s_stk._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in s_stk not found.')
            return
        try:
            new_position = list_of_items[index + 1]
            self.s_stk.set(new_position)
            self.eleana.set_selections('s_stk', index + 1)
        except IndexError:
            return
        self.grapher.plot_graph()

    @check_busy
    def s_stk_down_clicked(self):
        current_position = self.s_stk.get()
        list_of_items = self.s_stk._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in s_stk not found.')
            return
        if index == 0:
            return
        try:
            new_position = list_of_items[index - 1]
            self.s_stk.set(new_position)
            self.eleana.set_selections('s_stk', index - 1)
        except IndexError:
            return
        self.grapher.plot_graph()

    @check_busy
    def second_complex_clicked(self, value):
        self.eleana.set_selections('s_cpl', value)
        self.grapher.plot_graph()

    @check_busy
    def swap_first_second(self):
        first_pos = self.sel_first.get()
        second_pos = self.sel_second.get()
        first_stk = self.f_stk.get()
        second_stk = self.s_stk.get()
        if first_pos == 'None':
            self.firstComplex.grid_remove()
        if first_pos == 'None':
            self.secondComplex.grid_remove()
        self.sel_first.set(second_pos)
        self.sel_second.set(first_pos)
        self.first_selected(second_pos)
        self.second_selected(first_pos)
        self.f_stk.set(second_stk)
        self.s_stk.set(first_stk)
        self.f_stk_selected(second_stk)
        self.s_stk_selected(first_stk)
        self.grapher.plot_graph()

    @check_busy
    def second_to_result(self):
        current = self.sel_second.get()
        if current == 'None':
            return
        index = self.eleana.get_index_by_name(current)
        spectrum = copy.deepcopy(self.eleana.dataset[index])
        self.add_to_results(spectrum)

    @check_busy
    def add_to_results(self, spectrum):
        # Check the name if the same already exists in eleana.result_dataset
        list_of_results = []
        try:
            for each in self.eleana.results_dataset:
                list_of_results.append(each.name)
        except:
            pass
        name__ = self.generate_name_suffix(spectrum.name, list_of_results)
        spectrum.name = name__
        spectrum.name_nr = name__

        # Send to result and update lists
        self.eleana.results_dataset.append(spectrum)
        update.list_in_combobox('sel_result')
        update.list_in_combobox('r_stk')

        # Set the position to the last added item
        list_of_results = self.sel_result._values
        position = list_of_results[-1]
        self.sel_result.set(position)
        self.result_selected(position)

    ''' ***************************************
    *                RESULT                   *
    ****************************************'''

    @check_busy
    def result_show(self):
        self.eleana.set_selections('r_dsp', bool(self.check_result_show.get()))
        selection = self.sel_result.get()
        if selection == 'None':
            return
        self.result_selected(selection)

    @check_busy
    def result_selected(self, selected_value_text):
        if selected_value_text == 'None':
            self.eleana.set_selections('result', -1)
            self.resultComplex.grid_remove()
            self.resultStkFrame.grid_remove()
            self.grapher.plot_graph()
            return
        i = 0
        while i < len(self.eleana.results_dataset):
            name = self.eleana.results_dataset[i].name
            if name == selected_value_text:
                self.eleana.set_selections('result', i)
                break
            i += 1
        update.list_in_combobox('sel_result')
        update.list_in_combobox('r_stk')
        if self.eleana.results_dataset[self.eleana.selections['result']].complex:
            self.resultComplex.grid()
        else:
            self.resultComplex.grid_remove()
        self.eleana.selections['r_stk'] = 0
        self.grapher.plot_graph()

    @check_busy
    def result_up_clicked(self):
        current_position = self.sel_result.get()
        list_of_items = self.sel_result._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_result not found.')
            return
        try:
            new_position = list_of_items[index + 1]
            self.sel_result.set(new_position)
            self.result_selected(new_position)
        except IndexError:
            return
        self.grapher.plot_graph()

    @check_busy
    def result_down_clicked(self):
        current_position = self.sel_result.get()
        list_of_items = self.sel_result._values
        if current_position == 'None':
            return
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in sel_first not found')
            return
        try:
            new_position = list_of_items[index - 1]
            self.sel_result.set(new_position)
            self.result_selected(new_position)
        except IndexError:
            return
        self.grapher.plot_graph()

    @check_busy
    def r_stk_selected(self, selected_value_text):
        if selected_value_text in self.r_stk._values:
            index = self.r_stk._values.index(selected_value_text)
            self.eleana.set_selections('r_stk', index)
        else:
            return
        self.grapher.plot_graph()

    @check_busy
    def r_stk_up_clicked(self):
        current_position = self.r_stk.get()
        list_of_items = self.r_stk._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in r_stk not found.')
            return
        try:
            new_position = list_of_items[index + 1]
            self.r_stk.set(new_position)
            self.eleana.set_selections('r_stk', index + 1)
        except IndexError:
            return
        self.grapher.plot_graph()

    @check_busy
    def r_stk_down_clicked(self):
        current_position = self.r_stk.get()
        list_of_items = self.r_stk._values
        if current_position in list_of_items:
            index = list_of_items.index(current_position)
        else:
            print('Index in r_stk not found.')
            return
        if index == 0:
            return
        try:
            new_position = list_of_items[index - 1]
            self.r_stk.set(new_position)
            self.eleana.set_selections('r_stk', index - 1)
        except IndexError:
            return
        self.grapher.plot_graph()

    @check_busy
    def result_complex_clicked(self, value):
        self.eleana.set_selections('r_cpl', value)
        self.grapher.plot_graph()

    @check_busy
    def all_results_to_current_group(self):
        if len(self.eleana.results_dataset) == 0:
            return
        for each in self.eleana.results_dataset:
            result = copy.deepcopy(each)
            result.groups = [self.sel_group.get()]
            self.eleana.dataset.append(result)
        update.dataset_list()
        update.all_lists()
        added_item = self.eleana.dataset[-1].name_nr
        group = self.sel_group.get()
        self.group_selected(group)
        self.sel_first.set(added_item)
        self.first_selected(added_item)

    @check_busy
    def all_results_to_new_group(self):
        if len(self.eleana.results_dataset) == 0:
            return
        for each in self.eleana.results_dataset:
            result = copy.deepcopy(each)
            result.groups = [self.sel_group.get()]
            self.eleana.dataset.append(result)
        update.dataset_list()
        update.all_lists()
        added_item = self.eleana.dataset[-1].name_nr
        group = self.sel_group.get()
        self.group_selected(group)
        self.sel_first.set(added_item)
        self.first_selected(added_item)

    @check_busy
    def replace_first(self):
        if self.eleana.selections['result'] < 0:
            return
        index = self.eleana.selections['result']
        index_first = self.eleana.selections['first']
        result = copy.deepcopy(self.eleana.results_dataset[index])
        result.groups = [self.sel_group.get()]
        self.eleana.dataset.pop(index_first)
        self.eleana.dataset.insert(index_first, result)
        update.dataset_list()
        update.all_lists()
        group = self.sel_group.get()
        self.group_selected(group)
        name = self.eleana.dataset[index_first].name_nr
        self.first_selected(name)
        self.mainwindow.update_idletasks()
        self.sel_first.set(name)

    @check_busy
    def replace_group(self):
        group = self.eleana.selections['group']
        info = CTkMessagebox(master = self.mainwindow, title='Replace data in group', icon="warning", option_1="Cancel", option_2="Replace",
                             message=f'Are you sure you want to replace the data in the group: "{group}" with the results?')
        response = info.get()
        if response == 'Cancel':
            return
        self.delete_data_from_group(skip_questions=True)
        self.all_results_to_current_group()

    @check_busy
    def result_to_main(self):
        if self.eleana.selections['result'] < 0:
            return
        index = self.eleana.selections['result']
        result = copy.deepcopy(self.eleana.results_dataset[index])
        result.groups = [self.sel_group.get()]
        self.eleana.dataset.append(result)
        update.dataset_list()
        update.all_lists()
        added_item = self.eleana.dataset[-1].name_nr
        group = self.sel_group.get()
        self.group_selected(group)
        self.sel_first.set(added_item)
        self.first_selected(added_item)

    def delete_sel_result(self):
        index = self.eleana.selections['result']
        if index < 0:
            return
        self.eleana.results_dataset.pop(index)
        self.eleana.set_selections('result', -1)
        update.all_lists()
        update.gui_widgets()
        self.sel_result.set('None')
        self.grapher.plot_graph()

    def first_to_result(self, name = None):
        if name is not None:
            current = name
            skip_grapher = True
        else:
            current = self.sel_first.get()
            skip_grapher = False
        if current == 'None':
            return
        index = self.eleana.get_index_by_name(current)
        spectrum = copy.deepcopy(self.eleana.dataset[index])
        # Check the name if the same already exists in eleana.result_dataset
        list_of_results = []
        try:
            for each in self.eleana.results_dataset:
                list_of_results.append(each.name)
        except:
            pass
        # Create numbered name if similar exists in the Result Dataset
        name__ = self.generate_name_suffix(spectrum.name, list_of_results)
        spectrum.name = name__
        spectrum.name_nr = name__

        # Send to result and update lists
        self.eleana.results_dataset.append(spectrum)
        update.list_in_combobox('sel_result')
        update.list_in_combobox('r_stk')
        # Set the position to the last added item
        list_of_results = self.sel_result._values
        position = list_of_results[-1]
        self.sel_result.set(position)
        self.result_selected(position)
        if skip_grapher:
            return
        self.grapher.plot_graph()

    def generate_name_suffix(self, name, list_of_results):
        name_lists = []
        i = 0
        while i < len(list_of_results):
            from_list = list_of_results[i]
            from_list = re.split(r'(_#\d+$)', from_list)
            head = from_list[0]
            try:
                number = int(from_list[1][2:])
            except IndexError:
                number = 0
            name_lists.append({'name': head, 'nr': number})
            i += 1
        numbers = [-1]
        for each in name_lists:
            if each['name'] == name:
                numbers.append(each['nr'])
            else:
                numbers.append(-1)
        last_number = max(numbers)
        if last_number == 0:
            name = name + '_#1'
        elif last_number == -1:
            pass
        else:
            name = name + '_#' + str(last_number + 1)
        return name

    def get_indexes_by_name(self, names = None) -> list:
        if not names:
            return
        if type(names) == str:
            names = list(names)
        indexes = []
        for each in names:
            index = self.eleana.get_index_by_name(each)
            indexes.append(index)
        return indexes

    ''' *****************************************
    *            METHODS FOR MENU               *
    ******************************************'''


    # --------------------------------------------
    # MENU: Analysis
    # --------------------------------------------
    def integrate_region(self):
        ''' Integration of the selected range '''
        #self.integrate_region = IntegrateRegion(self, which = 'first')
        integrate_region = IntegrateRegion(self, which='first')

    def normalize(self):
        ''' Normalization of the amplitutes'''
        # self.normalize = Normalize(self, which = 'first')
        normalize = Normalize(self, which='first')

    def delete_selected_data(self, index_to_delete=None):
        av_data = self.sel_first._values
        av_data.pop(0)
        # Open dialog if index_to_delete was not set
        if index_to_delete is None:
            self.select_data = SelectData(master=app.mainwindow, title='Select data', group=self.eleana.selections['group'],
                                      items=av_data)
            response = self.select_data.get()
            if response == None:
                return
            # Get indexes of selected data to remove
            indexes = self.get_indexes_by_name(response)
        # Delete data with selected indexes or given by index_to_delete
        else:
            indexes = [index_to_delete]
        indexes.sort(reverse=True)
        for each in indexes:
            eleana.dataset.pop(each)
        # Set all data to None
        self.eleana.set_selections('first', -1)
        self.eleana.set_selections('second', -1)
        self.sel_first.set('None')
        self.sel_first.set('None')
        self.comparison_settings['indexes'] = []
        update.dataset_list()
        update.group_list()
        update.all_lists()
        update.gui_widgets()
        self.comparison_view()

    def delete_data(self, which, dialog=True):
        if which == 'result':
            self.delete_sel_result()
            return
        index = self.eleana.selections[which]
        if index < 0:
            return
        dialog = CTkMessagebox(master = self.mainwindow, title="Delete",
                                    message=f"Do you want to delete data selected in {which}?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = dialog.get()
        if response == 'No':
            return
        self.delete_selected_data(index_to_delete=index)

    def duplicate_data(self, which):
        index = self.eleana.selections[which]
        if index < 0:
            return
        if which == 'result':
            new_data = copy.deepcopy(self.eleana.results_dataset[index])
        else:
            new_data = copy.deepcopy(self.eleana.dataset[index])
        dialog = SingleDialog(master = self, title = 'Enter', label = 'New name', text = new_data.name)
        name = dialog.get()

        if not name:
            info = CTkMessagebox(master = self.mainwindow, title='', message='Name cannot be empty')
            return
        dataset = []
        try:
            if which == 'result':
                for each in self.eleana.result_dataset:
                    dataset.append(each.name)
            else:
                for each in self.eleana.result_dataset:
                    dataset.append(each.name)
        except:
            pass
        new_data.name = self.generate_name_suffix(name, dataset)
        if which == 'result':
            self.eleana.result_dataset.append(new_data)
        else:
            self.eleana.dataset.append(new_data)
        update.dataset_list()
        update.all_lists()

    def clear_results(self, skip_question = True):
        if not skip_question:
            quit_dialog = CTkMessagebox(master = self.mainwindow, title="Clear results",
                                        message="Are you sure you want to clear the entire dataset in the results?",
                                        icon="warning", option_1="No", option_2="Yes")
            response = quit_dialog.get()
        else:
            response = 'Yes'

        if response == "Yes":
            self.eleana.results_dataset = []
            self.eleana.selections['result'] = -1
            self.sel_result.configure(values=['None'])
            self.r_stk.configure(values=[])
            self.resultFrame.grid_remove()
            self.grapher.plot_graph()

    def gui_to_selections(self):
        ''' Get values from self.eleana.selections
            and update gui buttons accordingly'''
        select = self.eleana.selections
        self.sel_group.set(select['group'])

        # Set First, Second, Result visibility
        if select['f_dsp']:
            self.check_first_show.select()
        else:
            self.check_first_show.deselect()
        if select['s_dsp']:
            self.check_second_show.select()
        else:
            self.check_second_show.deselect()
        if select['r_dsp']:
            self.check_result_show.select()
        else:
            self.check_result_show.deselect()


        # Set Values in comboboxes
        # FIRST
        if select['first'] >= 0:
            f_name = self.eleana.dataset[select['first']].name_nr
            self.sel_first.set(f_name)
            if self.eleana.dataset[select['first']].type == 'stack 2D':
                stk_names = self.eleana.dataset[select['first']].stk_names
                stk_name = stk_names[select['f_stk']]
                self.f_stk.set(stk_name)
            if self.eleana.dataset[select['first']].complex:
                self.firstComplex.grid()
                self.firstComplex.set(select['f_cpl'])
            else:
                self.firstComplex.grid_remove()

        # SECOND
        if select['second'] >= 0:
            s_name = self.eleana.dataset[select['second']].name_nr
            self.sel_second.set(s_name)
            if self.eleana.dataset[select['second']].type == 'stack 2D':
                stk_names = self.eleana.dataset[select['second']].stk_names
                stk_name = stk_names[select['s_stk']]
                self.s_stk.set(stk_name)
            if self.eleana.dataset[select['second']].complex:
                self.secondComplex.grid()
                self.secondComplex.set(select['s_cpl'])
            else:
                self.secondComplex.grid_remove()

        # RESULT
        if select['result'] >= 0:
            r_name = self.eleana.results_dataset[select['result']].name
            self.sel_result.set(r_name)
            if self.eleana.results_dataset[select['result']].type == 'stack 2D':
                stk_names = self.eleana.result_dataset[select['result']].stk_names
                stk_name = stk_names[select['r_stk']]
                self.r_stk.set(stk_name)
            if self.eleana.results_dataset[select['result']].complex:
                self.resultComplex.grid()
                self.resultComplex.set(select['r_cpl'])
            else:
                self.resultComplex.grid_remove()

        self.grapher.plot_graph()

    def clear_dataset(self):
        quit_dialog = CTkMessagebox(master = self.mainwindow, title="Clear dataset",
                                    message="Are you sure you want to clear the entire dataset?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = quit_dialog.get()
        if response == "Yes":
            init.main_window()
            self.resultFrame.grid_remove()
            self.firstComplex.grid_remove()
            self.firstStkFrame.grid_remove()
            self.secondComplex.grid_remove()
            self.secondStkFrame.grid_remove()
            init.eleana_variables()
            self.grapher.plot_graph()

    def preferences(self):
        ''' Open window for editing preferences '''
        #preferences = PreferencesApp(self.mainwindow, self.grapher, self.color_theme, self.gui_appearence)
        preferences = PreferencesApp(self)
        response = preferences.get()
        if not response:
            return
        self.grapher.plot_graph()
        self.gui_appearence = response['gui_appearance']
        self.color_theme = response['color_theme']

    def load_project(self, event=None, recent=None):
        ''' Load project created with the Application '''
        project = load.load_project(recent)
        print(self.eleana.selections)
        if not project:
            return
        update.dataset_list()
        update.groups()
        update.all_lists()
        path_to_file = Path(self.eleana.paths['last_projects'][0])
        name = path_to_file.name
        app.mainwindow.title(name + ' - Eleana')
        self.eleana.paths['last_project_dir'] = str(Path(path_to_file).parent)
        main_menu.last_projects_menu()

        # Set settings to GUI
        # try:
        #     selected_value_text = self.eleana.dataset[self.eleana.selections['first']].name_nr
        #     self.first_selected(selected_value_text)
        #     self.sel_first.set(selected_value_text)
        # except:
        #     pass
        # try:
        #     selected_value_text = self.eleana.dataset[self.eleana.selections['second']].name_nr
        #     self.second_selected(selected_value_text)
        #     self.sel_second.set(selected_value_text)
        # except:
        #     pass
        # try:
        #     selected_value_text = self.eleana.results_dataset[self.eleana.selections['result']].name
        #     self.result_selected(selected_value_text)
        #     self.sel_result.set(selected_value_text)
        # except:
        #     pass
        # self.grapher.plot_graph()

        self.gui_to_selections()
        # try:
        #     selected_value_text = self.eleana.dataset[self.eleana.selections['first']].name_nr
        #     self.first_selected(selected_value_text)
        #     self.sel_first.set(selected_value_text)
        # except:
        #     pass
        # try:
        #     selected_value_text = self.eleana.dataset[self.eleana.selections['second']].name_nr
        #     self.second_selected(selected_value_text)
        #     self.sel_second.set(selected_value_text)
        # except:
        #     pass
        # try:
        #     selected_value_text = self.eleana.results_dataset[self.eleana.selections['result']].name
        #     self.result_selected(selected_value_text)
        #     self.sel_result.set(selected_value_text)
        # except:
        #     pass
        # self.grapher.plot_graph()

    def load_recent(self, selected_value_text):
        """ Load a project selected from Last Projects Menu"""
        index = selected_value_text.split('. ')
        index = int(index[0])
        index = index - 1
        recent = self.eleana.paths['last_projects'][index]
        self.load_project(recent=recent)
        self.eleana.paths['last_project_dir'] = Path(recent).parent
        self.grapher.plot_graph()

    def save_as(self, filename = None):
        file_saved = save.save_project(filename)
        if not file_saved:
            return
        else:
            last_projects = self.eleana.paths['last_projects']
            saved_path_string = str(file_saved)
            if saved_path_string in last_projects:
                index = last_projects.index(saved_path_string)
                del last_projects[index]
            last_projects.insert(0, str(saved_path_string))
        last_projects = last_projects[:20]
        # Write the list to eleana.paths
        self.eleana.paths['last_projects'] = last_projects
        self.eleana.paths['last_project_dir'] = Path(last_projects[0]).parent
        Save.save_settings_paths(self.eleana)
        # Perform update to place the item into menu
        main_menu.last_projects_menu()
        app.mainwindow.title(Path(last_projects[0]).name[:-4] + ' - Eleana')

    def save_current(self, event=None):
        win_title = self.mainwindow.title()
        if win_title == 'new project - Eleana':
            self.save_as(filename = None)
        else:
            file = win_title[:-13]
            file = file + '.ele'
            filename = Path(self.eleana.paths['last_project_dir'], file)
            self.save_as(filename)

    '''******************************************
              IMPORT EXTERNAL DATA             
    *********************************************'''

    def import_elexsys(self):
        ''' Open window that loads the spectra '''
        try:
            load.loadElexsys()
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
            last_in_list = self.sel_first._values
            self.first_selected(last_in_list[-1])

        except Exception as e:
            Error.show(info='Unable to import Elexsys file. Please verify that you have selected the correct format for import.', details=e)

    def import_EMX(self):
        try:
            load.loadEMX()
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import EMX file. Please verify that you have selected the correct format for import.', details=e)

    def import_magnettech1(self):
        try:
            load.loadMagnettech(1)
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Magnettech file. Please verify that you have selected the correct format for import.', details=e)

    def import_magnettech2(self):
        try:
            load.loadMagnettech(2)
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Magnettech file. Please verify that you have selected the correct format for import.', details=e)

    def import_adani_dat(self):
        try:
            load.loadAdaniDat()
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Adani file. Please verify that you have selected the correct format for import.', details=e)

    def import_shimadzu_spc(self):
        try:
            load.loadShimadzuSPC()
            update.dataset_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Shimadzu file. Please verify that you have selected the correct format for import.', details=e)

    def import_ascii(self, clipboard=None):
        try:
            load.loadAscii(clipboard)
            update.dataset_list()
            update.group_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Ascii file. Please verify that you have selected the correct format for import.', details=e)

    def load_excel(self):
        try:
            x = [['', ''], ['', '']]
            headers = ['A', 'B']
            empty = pandas.DataFrame(x, columns=headers)
            table = CreateFromTable(eleana_app=self.eleana, master=self.mainwindow, df=empty, loadOnStart='excel')
            response = table.get()
            update.dataset_list()
            update.group_list()
            update.all_lists()
            Save.save_settings_paths(self.eleana)
        except Exception as e:
            Error.show(info='Unable to import Excel file. Please verify that you have selected the correct format for import.', details=e)

    def quick_copy(self):
        curves = self.grapher.ax.get_lines()
        the_longest = 0
        collected_list = []

        for curve in curves:
            label = curve.get_label()
            x_data = [str(element) for element in curve.get_xdata()]
            if x_data:
                x_data.insert(0, f'{label} [X]')
                collected_list.append(x_data)
                y_data = [str(element) for element in curve.get_ydata()]
                y_data.insert(0, f'{label} [Y]')
                collected_list.append(y_data)
                length = len(x_data)

                if length > the_longest:
                    the_longest = length

        # Replenish shorter lists with empty strings
        even_collected_list = []
        for row in collected_list:
            row_length = len(row)
            diff = the_longest - row_length
            if diff > 0:
                row.extend([""] * diff)
            even_collected_list.append(row)

        # Transpose list
        transposed_data = list(map(list, zip(*even_collected_list)))
        text_output = "\n".join("\t".join(row) for row in transposed_data)
        self.mainwindow.clipboard_clear()
        self.mainwindow.clipboard_append(text_output)
        self.mainwindow.update()

    def quick_paste(self, event=None):
        text = self.mainwindow.clipboard_get()
        self.import_ascii(text)

    def export_first(self):
        export.csv('first')

    def export_group(self):
        export.group_csv(self.eleana.selections['group'])

    # --- Quit (also window close by clicking on X)
    def close_application(self, event=None):
        global list_of_subprogs
        quit_dialog = CTkMessagebox(master = self.mainwindow, title="Quit", message="Do you want to close the program?",
                                    icon="warning", option_1="No", option_2="Yes")
        response = quit_dialog.get()
        if response == "Yes":
            # # Save current settings:
            Save.save_settings_paths(self.eleana)
            Save.save_preferences(self.eleana, self, self.grapher)
            self.mainwindow.iconify()
            # Close all subprograms from the list
            self.close_all_subprogs()
            # Close all static_plot windows from self.eleana.active_static_windows
            if self.eleana.active_static_plot_windows:
                for window_nr in self.eleana.active_static_plot_windows:
                    close_cmd = "self.grapher.static_plot_" + str(window_nr) + ".cancel()"
                    try:
                        exec(close_cmd)
                    except:
                        print("Error: " + close_cmd)
            self.mainwindow.destroy()

    def close_all_subprogs(self):
        for each in list_of_subprogs:
            close_cmd = 'self.' + each[0] + '.' + each[1] + '()'
            try:
                exec(close_cmd)
            except:
                pass

    def edit_values_in_table(self, which ='first'):
        if which == 'first' or which == 'second':
            index_in_data = self.eleana.selections[which]
        if index_in_data < 0:
            Error.show(info = 'No data selected to edit.')
            return

        data = self.eleana.dataset[index_in_data]
        x_header = f"{data.parameters['name_x']} [{data.parameters['unit_x']}]"
        if data.type == 'single 2D' or data.type == "":
            y_header = f"{data.parameters.get('name_y', '')} [{data.parameters.get('unit_y', '')}]"
            headers = [x_header, y_header]
        elif data.type == 'stack 2D':
            headers = [x_header]
            headers.extend(data.stk_names)
        else:
            Error.show(info = "Data type not specified. Expected 'single 2D' or 'stack 2D'")
            return

        table = EditValuesInTable(eleana_app=self.eleana,
                                master=self.mainwindow,
                                x = data.x,
                                y = data.y,
                                name = data.name,
                                window_title = f"Edit {data.name}",
                                column_names = headers,
                                complex = data.complex
                                  )
        response = table.get()
        if response is None:
            return
        data.x = response[0]
        data.y = response[1]
        update.dataset_list()
        update.group_list()
        update.all_lists()
        self.grapher.plot_graph()

    def notes(self):
        #self.notepad = Notepad(master=self.mainwindow, title="Edit notes", text=self.eleana.notes)
        #response = self.notepad.get()

        notepad = Notepad(master=self.mainwindow, title="Edit notes", text=self.eleana.notes)
        response = notepad.get()
        if response == None:
            return
        else:
            self.eleana.notes = response

    def create_new_group(self):
        # self.group_create = Groupcreate(self.mainwindow, eleana)
        # response = self.group_create.get()
        group_create = Groupcreate(self.mainwindow, eleana)
        response = group_create.get()

        update.list_in_combobox('sel_group')

    def create_from_table(self):
        headers = ['A', 'B', 'C']
        date = [['', '', ''],['', '', ''],['', '', ''],['', '', ''],['', '', ''],['', '', '']]
        df = pandas.DataFrame(columns=headers, data=date)
        name = 'new'
        spreadsheet = CreateFromTable(self.eleana, self.mainwindow, df=df, name=name,
                                           group=self.eleana.selections['group'])
        response = spreadsheet.get()
        update.group_list()
        update.dataset_list()
        update.all_lists()


    def first_to_group(self):
        if self.eleana.selections['first'] < 0:
            return
        group_assign = Groupassign(master=app, which='first')
        response = group_assign.get()
        update.group_list()
        update.all_lists()

    def second_to_group(self):
        if self.eleana.selections['second'] < 0:
            return
        group_assign = Groupassign(master=app, which='second')
        response = group_assign.get()

    def create_simple_static_plot(self):
        '''
        Get data from the current graph and create a new data for simple graph
        that will be used to display independet matplotlib window
        '''
        if bool(self.switch_comparison.get()) == True:
            info = CTkMessagebox(master = self.mainwindow, title="Info", message="This function is not yet available for comparison view.")
            return
        static_plot = self.grapher.get_static_plot_data()
        if not static_plot:
            info = CTkMessagebox(master = self.mainwindow, title="Info", message="An error occurred or there is no data for graph creation.")
            return
        dialog = SingleDialog(master=app, title='Enter a name for the graph', label='Enter the graph name', text='')
        name = dialog.get()
        if not name:
            return
        static_plot['name'] = name
        self.eleana.static_plots.append(static_plot)
        main_menu.create_showplots_menu()
        self.grapher.show_static_graph_window(len(self.eleana.static_plots)-1)

    def clear_selected_ranges(self):
        self.grapher.clear_selected_ranges()
        self.grapher.clear_all_annotations()

    def delete_simple_static_plot(self):
        '''
        Opens window to ask which plots
        from created Static Plots will be removed
        '''
        plots = self.eleana.static_plots
        if not plots:
            return
        av_plots = []
        for plot in plots:
            av_plots.append(plot['name_nr'])
        self.select_items = SelectItems(master=app.mainwindow, title='Select plots',
                                  items=av_plots)
        names = self.select_items.get()
        if not names:
            return
        to_delete = []
        for name in names:
            to_delete.append(names.index(name))
        to_delete.sort(reverse=True)
        for i in to_delete:
            self.eleana.static_plots.pop(i)
        main_menu.create_showplots_menu()

    def xy_distance(self):
        xy_distance = DistanceRead(self, which='first')

    def trim_data(self):
        subprog_trim_data = TrimData(self, which="first")

    def polynomial_baseline(self):
        subprog_polynomial_baseline = PolynomialBaseline(self, which='first')

    def spline_baseline(self):
        subprog_spline_baseline = SplineBaseline(self, which='first')

    def filter_savitzky_golay(self):
        subprog_sav_gol = SavGol(self, which = 'first')

    def filter_fft_lowpass(self):
        subprog_fft_lowpass = FFTFilter(self, which = 'first')

    def pseudomodulation(self):
        subprog_pseudomodulation = PseudoModulation(self, which = 'first')

    def fast_fourier_transform(self):
        subprog_fft = FastFourierTransform(self, which = 'first')

    def spectra_subtraction(self):
        subprog_spectra_subtraction = SpectraSubtraction(self, which = 'first')

    # --------------------------------------------
    # MENU: EPR
    # --------------------------------------------

    def epr_b_to_g(self):
        subprog_epr_b_to_g = EPR_B_to_g(self)

    '''***********************************************
    *           GRAPH SWITCHES AND BUTTONS           *
    ***********************************************'''

    def switch_autoscale_x(self):
        self.grapher.plot_graph()

    def switch_autoscale_y(self):
        self.grapher.plot_graph()

    def set_log_scale_x(self):
        self.grapher.plot_graph()

    def set_log_scale_y(self):
        self.grapher.plot_graph()

    def indexed_x(self):
        self.grapher.indexed_x = bool(self.check_indexed_x.get())
        self.grapher.plot_graph()

    def invert_x_axis(self):
        self.grapher.inverted_x_axis = bool(self.check_invert_x.get())
        self.grapher.plot_graph()

    '''***********************************************
    *                    CURSORS                     *
    ***********************************************'''
    def clear_cursors(self):
        self.grapher.clear_all_annotations()

    def sel_graph_cursor(self, value, clear_annotations=True):
        if clear_annotations:
            self.grapher.clear_all_annotations(True)
        self.grapher.current_cursor_mode['label'] = value
        self.grapher.plot_graph()
        self.grapher.cursor_on_off()

    '''***********************************************
    *           METHODS FOR CONTEXT MENU             *
    ***********************************************'''

    def stack_to_group(self, which):
        index = self.eleana.selections[which]
        if index < 0:
            return
        data = copy.deepcopy(self.eleana.dataset[index])
        if not data.type == 'stack 2D':
            CTkMessagebox(master = self.mainwindow, title="Conversion to group", message="The data you selected is not a 2D stack")
        else:
            #self.convert_stack_to_group = StackToGroup(app, which)
            #response = self.convert_stack_to_group.get()

            convert_stack_to_group = StackToGroup(app, which)
            response = convert_stack_to_group.get()
            if response == None:
                 return
            update.dataset_list()
            update.group_list()
            update.all_lists()

    def delete_single_stk_data(self, which):
        ''' Remove single data from stk stack '''
        if which == 'first':
            data_index = self.eleana.selections['first']
            stk_index = self.eleana.selections['f_stk']
        elif which == 'second':
            data_index = self.eleana.selections['second']
            stk_index = self.eleana.selections['s_stk']
        else:
            return

        # data_y = self.eleana.dataset[data_index].y
        # data_z = self.eleana.dataset[data_index].z
        # data_names = self.eleana.dataset[data_index].stk_names
        # if data_y.size == 0:
        #     # Already empty np.array. Return
        #     return

        # # Remove stk data from dataset.y
        # new_y = np.delete(data_y, stk_index, axis=0)
        # self.eleana.dataset[data_index].y = new_y

        # # Remove values from z axis of stk data
        # new_z = np.delete(data_z, stk_index)
        # self.eleana.dataset[data_index].z = new_z

        # # Remove stk names
        # del self.eleana.dataset[data_index].stk_names[stk_index]

        data_stack: BaseDataModel = self.eleana.dataset[data_index]
        data_stack.remove_from_stack_by_index(stk_index)

        if which == 'first':
            self.eleana.selections['f_stk'] = 0
        elif which == 'second':
            self.eleana.selections['s_stk'] = 0

        # Update all GUI elements
        update.dataset_list()
        update.all_lists()
        self.grapher.plot_graph()

    def rename_data(self, which):
        index = self.eleana.selections[which]
        index_f = self.eleana.selections['first']
        index_s = self.eleana.selections['second']
        index_r = self.eleana.selections['result']
        if index < 0:
            return
        name = self.eleana.dataset[index].name
        if which == 'first':
            title = 'Rename First'
        elif which == 'second':
            title = 'Rename Second'
        elif which == 'result':
            title = 'Rename Result'
            name = self.eleana.results_dataset[index_r].name
        #self.single_dialog = SingleDialog(master=app, title=title, label='Enter new name', text=name)
        #response = self.single_dialog.get()

        single_dialog = SingleDialog(master=app, title=title, label='Enter new name', text=name)
        response = single_dialog.get()

        if response == None:
            return
        if not which == 'result':
            self.eleana.dataset[index].name = response
            update.dataset_list()
            update.group_list()
            update.all_lists()
            if index_f >= 0:
                self.sel_first.set(self.eleana.dataset[index_f].name_nr)
            if index_s >= 0:
                self.sel_second.set(self.eleana.dataset[index_s].name_nr)
        else:
            self.eleana.results_dataset[index_r].name = response
            self.eleana.results_dataset[index_r].name_nr = response
            update.dataset_list()
            update.all_lists()
        if index_r >= 0:
            self.sel_result.set(self.eleana.results_dataset[index_r].name_nr)

    def edit_comment(self, which):
        index = self.eleana.selections[which]
        if index < 0:
            return
        comment = self.eleana.dataset[index].comment
        name = 'Comment to: ' + str(self.eleana.dataset[index].name_nr)
        text = Notepad(self.mainwindow, title=name, text=comment)
        response = text.get()
        self.eleana.dataset[index].comment = response

    def edit_parameters(self, which='first'):
        idx = self.eleana.selections.get(which, - 1)
        if idx < 0:
            return
        par_to_edit = self.eleana.dataset[idx].parameters
        name_nr = self.eleana.dataset[idx].name_nr
        #self.edit_par = EditParameters(self.mainwindow, parameters=par_to_edit, name=name_nr)
        #response = self.edit_par.get()
        edit_par = EditParameters(self.mainwindow, parameters=par_to_edit, name=name_nr)
        response = edit_par.get()

        if response:
            self.eleana.dataset[idx].parameters = response
        else:
            return

    def execute_command(self, event):
        if event.keysym == "Up":
            try:
                previous = self.command_history['index'] - 1
                self.command_history['index'] = previous
                previous_command = self.command_history['lines'][previous]
                self.command_line.delete(0, "end")
                self.command_line.insert(0, previous_command)
            except:
                pass
            return
        if event.keysym == "Down":
            try:
                previous = self.command_history['index'] + 1
                self.command_history['index'] = previous
                previous_command = self.command_history['lines'][previous]
                self.command_line.delete(0, "end")
                self.command_line.insert(0, previous_command)
            except:
                pass
            return
        if event.keysym == "Return":
            command = self.command_line.get()
            self.command_history['lines'].append(command)
            self.command_history['index'] = len(self.command_history['lines']) - 1
            new_log = '\n>>> ' + command
            self.log_field.insert("end", new_log)
            self.command_line.delete(0, "end")
            error, executable_command = self.commandprocessor.process_script(command)
            print(command)
            print(executable_command)
            stdout_backup = sys.stdout
            sys.stdout = io.StringIO()
            try:
                eval(executable_command, globals(), locals())
                output = sys.stdout.getvalue()
            except Exception as e:
                output = f"Error: {e}"
            finally:
                sys.stdout = stdout_backup
            new_log = '\n' + output
            self.log_field.insert("end", new_log)
            return output

    def copy_to_clipboard(self, event):
        print('Copy to clipboard. (1395)')

''' STARTING THE APPLICATION '''

# Create general main instances for the program
if not DEVEL:
    # Switch off the error display in final product
    if os.name == 'posix':  # Unix/Linux/macOS
        sys.stderr = open(os.devnull, 'w')
    elif os.name == 'nt':  # Windows
        sys.stderr = open('nul', 'w')

    # Switch off nupy RankWarnings in Numpy
    import warnings
    warnings.simplefilter('ignore', np.exceptions.RankWarning)



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

    ''' Create Main instances '''
    eleana = Eleana(version=ELEANA_VERSION, devel=DEVEL)
    sound = Sound()
    cmd = CommandProcessor()

    # Create GUI
    app = MainApp(eleana, cmd)  # This is GUI
    main_menu = MainMenu(app)
    grapher = Grapher(main_menu)
    app.set_grapher(grapher)

    load = Load(main_menu)
    save = Save(app)
    export = Export(app)
    init = Init(main_menu)
    context_menu = ContextMenu(app)
    update = Update(main_menu)  # This contains methods for update things like lists, settings, gui, groups etc.
    app.set_update(update)

    # Initialize basic settings: geometry, icon, graph, binding, etc
    init.main_window()
    init.paths(update)
    init.folders()
    init.graph()

    # Command Line and tests

    # Create Graph canvas
    grapher.plot_graph()
    # Hide or show widgets in GUI
    update.gui_widgets()
    update.all_lists()

    # Set graph Frame scalable
    app.graphFrame.columnconfigure(0, weight=1)
    app.graphFrame.rowconfigure(0, weight=1)
    main_menu.last_projects_menu()

    app.run()
